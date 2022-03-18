import sounddevice as sd
from scipy.io.wavfile import write
from google.cloud import speech
from pydub import AudioSegment
import pydub
import io

pydub.AudioSegment.ffmpeg = 'D:\ffmpeg-5.0-essentials_build\ffmpeg-5.0-essentials_build\bin'

client = speech.SpeechClient.from_service_account_json(
    'watolink-speech-to-text-b41c581cbd15.json'
)


freq = 44100

duration = 2

print("Talk")

recording = sd.rec(int(duration * freq), samplerate=freq, channels=2)

sd.wait()

print("Stop")

write("prompt.wav", freq, recording)
src = "prompt.wav"



sound = AudioSegment.from_mp3(src)

# sound.export("/AudioFiles/prompt.mp3")

# with open("/AudioFiles/prompt.mp3", "rb") as audio_file:
#     content = audio_file.read()



# audio = speech.RecognitionAudio(content=content)

# config = speech.RecognitionConfig(
#     encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
#     sample_rate_hertz=44100,
#     language_code="en-US",
# )

# operation = client.long_running_recognize(config=config, audio=audio)

# print("Waiting for operation to complete...")
# response = operation.result(timeout=90)
