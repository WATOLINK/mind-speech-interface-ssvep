import os
import openai
from dotenv import load_dotenv
from speech_to_text import SpeechToText
from prediction import OpenAI

s = SpeechToText()
text = s.speechToText()

o = OpenAI()

prompt = "Question: " + text + "?\nAnswer:"

res = o.predictedSentences(prompt, num_results=5)

print(res)
