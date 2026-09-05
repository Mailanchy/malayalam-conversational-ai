import os
from dotenv import load_dotenv
load_dotenv()

import speech_recognition as sr
import boto3
import os
import re


class MalayalamSpeechRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        # Initialize AWS Translate client (Using hardcoded credentials)
        self.translate_client = boto3.client('translate',
            region_name='us-east-1',  # Replace with your AWS region
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),  # Your AWS access key
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")  # Your AWS secret key
        )
    def extract_info(self, filename):
        """Extracts speaker number and start time from filename"""
        match = re.search(r"SPEAKER_(\d+)_(\d+\.\d+).wav", filename)
        if match:
            speaker = match.group(1)  # Extract speaker number
            start_time = float(match.group(2))  # Extract start time
            return speaker, start_time
        return None, None


    def transcribe(self, audio_files):
        """Transcribes sorted audio files with speaker labels and maintains order"""
        transcriptions = []  # Store transcriptions


        # Ensure audio_files is a list
        if isinstance(audio_files, str):  
            audio_files = [audio_files]


        for file_path in audio_files:
            speaker, start_time = self.extract_info(file_path)  # Get speaker info
            with sr.AudioFile(file_path) as source:
                print(f"🎤 Processing {file_path} ...")
                audio = self.recognizer.record(source)  # Load full audio file


            try:
                text = self.recognizer.recognize_google(audio, language="ml-IN")
                print(f"✅ Transcribed {file_path}: {text}")
                transcriptions.append(f"Speaker {speaker}: {text}")  # Add speaker label
            except sr.UnknownValueError:
                transcriptions.append(f"Speaker {speaker}: ⚠ Could not understand audio")
            except sr.RequestError:
                transcriptions.append(f"Speaker {speaker}: ⚠ Speech recognition error")


        return "\n".join(transcriptions)  # Combine transcriptions in correct order


   
    def translate_to_english(self, malayalam_text):
        try:
            # Call AWS Translate
            response = self.translate_client.translate_text(
                Text=malayalam_text,
                SourceLanguageCode='ml',  # Malayalam
                TargetLanguageCode='en'   # English
            )
            return response['TranslatedText']
        except Exception as e:
            print(f"⚠ Translation error: {str(e)}")
            return "⚠ Translation failed"


def main():
    recognizer = MalayalamSpeechRecognizer()


    # Collect all split audio files
    split_audio_files = [file for file in os.listdir() if file.endswith(".wav")]


    # Handle case where no files are found
    if not split_audio_files:
        print("⚠ No audio files found for transcription.")
        return


    print("\n⏳ Passing files to Speech-to-Text module...")
    final_transcription = recognizer.transcribe(split_audio_files)


    print("\n📜 Final Transcription Output:")
    print(final_transcription)


    # Only translate if transcription was successful
    if final_transcription and "⚠" not in final_transcription:
        english_text = recognizer.translate_to_english(final_transcription)
        print("\n🇺🇸 English Translation:")
        print(english_text)
    else:
        print("\n⚠ Skipping translation due to transcription errors.")


if __name__ == '__main__':
    main()