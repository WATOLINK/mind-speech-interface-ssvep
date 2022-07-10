from pyexpat import model
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


freq = 44100  # Sample Rate Frequency

duration = 2  # Duration of the clip in seconds

print("Talk")

recording = sd.rec(int(duration * freq), samplerate=freq,
                   channels=1, dtype='int16')

sd.wait()

print("Stop")

# Stores the recording at the same level in a file named prompt.wav
write("prompt.wav", freq, recording)

with open("prompt.wav", "rb") as audio_file:
    content = audio_file.read()

audio = speech.RecognitionAudio(content=content)

config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    audio_channel_count=1,
    language_code="en-US",
    sample_rate_hertz=44100,
)

# Sends the audio to the Cloud Speech to Text API
operation = client.long_running_recognize(config=config, audio=audio)

print("Waiting for operation to complete...")
response = operation.result(timeout=90)

for result in response.results:
    # The first alternative is the most likely one for this portion.
    print(u"Transcript: {}".format(result.alternatives[0].transcript))
    print("Confidence: {}".format(result.alternatives[0].confidence))
