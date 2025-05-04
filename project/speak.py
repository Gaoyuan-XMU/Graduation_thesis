import asyncio
from edge_tts import Communicate

async def generate_tts(text, output_path):
    communicate = Communicate(text, voice="zh-CN-XiaoxiaoNeural")  # 可换成别的中文声音
    await communicate.save(output_path)

def text_to_speech(input_path, output_path):
    with open(input_path, 'r') as f:
        text = f.read()
    asyncio.run(generate_tts(text, output_path))
    return output_path
