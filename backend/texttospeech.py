import os
from gtts import gTTS
import base64
from pydub import AudioSegment

def text_to_speech(text):
    # Get absolute path
    base_dir = os.path.dirname(os.path.abspath(__file__))
    audio_dir = os.path.join(base_dir, "audio")
    os.makedirs(audio_dir, exist_ok=True)

    mp3_path = os.path.join(audio_dir, "output.mp3")
    wav_path = os.path.join(audio_dir, "converted.wav")

    # Save MP3
    tts = gTTS(text=text, lang="ml")
    tts.save(mp3_path)

    # Check it actually saved
    if not os.path.exists(mp3_path):
        raise Exception(f"TTS failed. File not found: {mp3_path}")

    # Convert MP3 to WAV
    sound = AudioSegment.from_mp3(mp3_path)
    sound.export(wav_path, format="wav")

    # Encode to base64
    with open(wav_path, "rb") as wav_file:
        b64 = base64.b64encode(wav_file.read()).decode("utf-8")

    return b64



# from gtts import gTTS
# import base64
# from pydub import AudioSegment

# def text_to_speech(text):
#     tts = gTTS(text=text, lang="ml")  # Malayalam language
#     tts.save("audio/output.mp3")  # Save the audio file
#     sound = AudioSegment.from_mp3("audio/output.mp3")
#     sound.export("audio/converted.wav", format="wav")
#     with open("audio/converted.wav", "rb") as wav_file:
#         wav_bytes = wav_file.read()
#         base64_bytes = base64.b64encode(wav_bytes)
#         base64_string = base64_bytes.decode('utf-8')
#     return base64_string