import os
from dotenv import load_dotenv
load_dotenv()

import wave
import numpy as np
import sounddevice as sd
from pyannote.audio import Pipeline
import os
from stt import MalayalamSpeechRecognizer
from llm import get_response
from etom import EnglishToMalayalamTranslator
from etomsuper import supernova_malayalam_translator
from texttospeech import text_to_speech
import re

# For deleting previously processed audio files
for files in os.listdir():
    if files.endswith(".wav"):
        os.remove(files)

# Set recording parameters
sample_rate = 44100
duration = 10

print("Recording...")
recording = sd.rec(int(sample_rate * duration), samplerate=sample_rate, channels=1, dtype=np.int16)
sd.wait()
print("Completed recording")

# Convert recording to float and normalize
recording_float = recording.astype(np.float32)
recording_norm = recording_float / np.max(np.abs(recording_float))

# Save the full normalized recording as a WAV file (convert back to int16)
with wave.open('firstRecord.wav', 'wb') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)  # 2 bytes for int16
    wf.setframerate(sample_rate)
    wf.writeframes((recording_norm * 32767).astype(np.int16).tobytes())
# print("Recorded a .wav audio file and saved")

# Load the speaker diarization pipeline
pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1",
    use_auth_token=os.getenv("HF_AUTH_TOKEN")
)
diarization = pipeline("firstRecord.wav")

prev_speaker = None
start_sample = None
time_marker = None

# Iterate over each diarization segment
for turn, _, speaker in diarization.itertracks(yield_label=True):
    print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")
    if prev_speaker is None:
        # First segment initialization
        start_sample = int(turn.start * sample_rate)
        end_sample = int(turn.end * sample_rate)
        prev_speaker = speaker
        time_marker = turn.start
    elif prev_speaker == speaker:
        # Extend the current segment if the speaker is the same
        end_sample = int(turn.end * sample_rate)
    else:
        # Save the segment for the previous speaker
        segment = recording_norm[start_sample:end_sample+1]
        segment_int16 = (segment * 32767).astype(np.int16)
        filename = f"{prev_speaker}_{time_marker:.1f}.wav"
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(segment_int16.tobytes())
        # Update for the new speaker segment
        start_sample = int(turn.start * sample_rate)
        end_sample = int(turn.end * sample_rate)
        prev_speaker = speaker
        time_marker = turn.start

# Save the last speaker segment if one exists
if prev_speaker is not None:
    segment = recording_norm[start_sample:end_sample+1]
    segment_int16 = (segment * 32767).astype(np.int16)
    filename = f"{prev_speaker}_{time_marker:.1f}.wav"
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(segment_int16.tobytes())

# Collecting all audio files into one list
# Function to extract speaker and start time from filename
def extract_info(filename):
    match = re.search(r"SPEAKER_(\d+)_(\d+\.\d+).wav", filename)
    if match:
        speaker = match.group(1)  # Speaker number
        start_time = float(match.group(2))  # Start time
        return speaker, start_time
    return None, None
split_audio_files = [file for file in os.listdir() if file.startswith("SPEAKER_") and file.endswith(".wav")]
sorted_audio_files = sorted(split_audio_files, key=lambda x: extract_info(x)[1]) #sorted(iterable, key=lambda element: some_function(element)[index])

#passing it to stt module
transcriber = MalayalamSpeechRecognizer()
malayalam_txt = transcriber.transcribe(sorted_audio_files)
print(malayalam_txt)
if malayalam_txt and "⚠" not in malayalam_txt:
     english_text = transcriber.translate_to_english(malayalam_txt)
     print(f"Eng: {english_text}")

#Passing it to llm
# print("\n🤖 Sending to LLM for Response...")
llm_response = get_response(english_text)  # Call LLM function
print("\n🧠 LLM Response:")
print(f"LLM: {llm_response}")

#PAssing it to trasnlate to malayalam

# translator = EnglishToMalayalamTranslator()
# malayalam_llm_response = translator.translate_to_malayalam(llm_response)
# # print("\n🌍 Malayalam LLM Response:")
# print(f"MAl llm:{malayalam_llm_response}")


# text_to_speech(malayalam_llm_response)

malayalam_llm_response = supernova_malayalam_translator(llm_response)
text_to_speech(malayalam_llm_response)
print("\n🔊 Malayalam speech generated: output.mp3")

