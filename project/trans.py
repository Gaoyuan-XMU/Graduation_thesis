import whisper
import opencc

def transcribe_audio(audio_path, output_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    cc = opencc.OpenCC("t2s")
    simplified_text = cc.convert(result['text'])
    
    with open(output_path, 'w') as f:
        f.write(simplified_text)
    return simplified_text