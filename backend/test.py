from pydub import AudioSegment
sound = AudioSegment.from_mp3("output.mp3")
sound.export("converted.wav", format="wav")