import gradio as gr
import os
import subprocess
import glob
from trans import transcribe_audio
from request import query_dify
from speak import text_to_speech

CONFIG = {
    "transcript_path": os.path.join(os.getcwd(), "output", "transcript.txt"),
    "answer_path": os.path.join(os.getcwd(), "output", "answer.txt"),
    "speech_path": os.path.join(os.getcwd(), "output", "answer.mp3"),
    "api_key": "app-gzynEHxAF8Djn8QkWwNMRtcC"
}

SADTALKER_PATH = "G:/Last/AI_Digital_Human"  # ⚠️ 替换为你本地实际路径
os.makedirs("output", exist_ok=True)

def validate_file(path):
    return bool(path and os.path.exists(path) and os.path.getsize(path) > 0)

def generate_video_with_sadtalker(image_path, audio_path, output_dir):
    venv_python = os.path.join(SADTALKER_PATH, "venv", "Scripts", "python.exe")
    inference_script = os.path.join(SADTALKER_PATH, "inference.py")

    if not os.path.exists(venv_python):
        raise RuntimeError(f"虚拟环境未找到: {venv_python}")

    cmd = [
        venv_python,
        inference_script,
        "--driven_audio", audio_path,
        "--source_image", image_path,
        "--result_dir", output_dir
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Sadtalker 执行失败: {result.stderr}")

    return find_latest_mp4(output_dir)

def find_latest_mp4(output_dir):
    mp4_files = glob.glob(os.path.join(output_dir, "**", "*.mp4"), recursive=True)
    if not mp4_files:
        raise RuntimeError("未找到任何 .mp4 文件")
    return max(mp4_files, key=os.path.getctime)

def process_pipeline(history, audio_path, source_image):
    try:
        if not validate_file(audio_path):
            raise RuntimeError("未收到有效的音频文件")

        transcript = transcribe_audio(audio_path, CONFIG["transcript_path"])
        if not validate_file(CONFIG["transcript_path"]):
            raise RuntimeError("转写文件生成失败")

        answer = query_dify(CONFIG["transcript_path"], CONFIG["answer_path"], CONFIG["api_key"])
        if not validate_file(CONFIG["answer_path"]):
            raise RuntimeError("API响应文件生成失败")

        text_to_speech(CONFIG["answer_path"], CONFIG["speech_path"])
        if not validate_file(CONFIG["speech_path"]):
            raise RuntimeError("语音文件生成失败")

        if not source_image or not os.path.exists(source_image):
            raise RuntimeError("请上传有效的图像文件")

        output_dir = os.path.join(os.getcwd(), "output")
        video_path = generate_video_with_sadtalker(source_image, CONFIG["speech_path"], output_dir)

        new_history = history + [(transcript, answer)]
        return new_history, video_path, ""
    except Exception as e:
        return history, None, f"❌ 错误: {str(e)}"

def render_autoplay_video(history, video_path, error):
    if video_path:
        html = f"""
        <video width='100%' autoplay playsinline controls>
            <source src='file/{video_path}' type='video/mp4'>
            您的浏览器不支持 video 标签。
        </video>
        """
        return history, html, error
    return history, "", error

def reset_conversation():
    try:
        if os.path.exists("output/conversation_id.txt"):
            os.remove("output/conversation_id.txt")
        return [], "", "对话已重置"
    except Exception as e:
        return [], "", f"重置失败: {str(e)}"

with gr.Blocks(title="数字人在线交互平台", theme="soft") as demo:
    gr.Markdown("""
    # 🤖 数字人在线交互平台
    欢迎来到实时语音对话系统，上传人物图像并与数字人对话。
    """)

    with gr.Row():
        with gr.Column(scale=2):
            gr.Markdown("### 💬 对话历史")
            history = gr.Chatbot(label="", height=400).style(container=True, height=400)
            error_output = gr.Markdown(value="", elem_id="status_text", visible=True)

        with gr.Column(scale=1):
            gr.Markdown("### 🖼️ 人物图像上传")
            source_image_input = gr.Image(label="上传头像照片用于驱动（支持 JPG/PNG）", type="filepath")

            gr.Markdown("### 🎙️ 语音输入")
            audio_input = gr.Audio(source="microphone", type="filepath", label="点击录音")

            submit_btn = gr.Button("📤 提交语音", variant="primary")
            reset_btn = gr.Button("🔄 重置对话", variant="secondary")

            gr.Markdown("### 📽️ 合成视频预览")
            video_output = gr.HTML(label="合成视频")

    video_path_state = gr.State()

    submit_btn.click(
        fn=process_pipeline,
        inputs=[history, audio_input, source_image_input],
        outputs=[history, video_path_state, error_output]
    ).then(
        fn=render_autoplay_video,
        inputs=[history, video_path_state, error_output],
        outputs=[history, video_output, error_output]
    )

    reset_btn.click(
        fn=reset_conversation,
        outputs=[history, video_output, error_output]
    )

if __name__ == "__main__":
    demo.launch(server_port=7860, show_error=True, enable_queue=True)
