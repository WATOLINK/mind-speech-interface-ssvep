import speech_recognition as sr
import os
import openai
from dotenv import load_dotenv

# loads environment variables, contact jackie if you are missing .env
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY


# using speech to text to get prompt
r = sr.Recognizer() 

mic = sr.Microphone(device_index=0) # default mic is used if device_index=0 or NULL

with mic as source: 
   audio = r.listen(source) 

try:
   text = r.recognize_google(audio)
except:
   print("Error")

prompt = "Question: " + text + "?\nAnswer:"

while 1:
   print(prompt)
   res = openai.Completion.create(engine="curie", max_tokens=1, temperature=1, n = 1, prompt = prompt, logprobs=3)
   wordDict = res["choices"][0]["logprobs"]["top_logprobs"][0]
   wordList = []
   terminalUI = ""
   
   for index, key in enumerate(wordDict):
      terminalUI = terminalUI + str(index) + ": " + key + "\n"
      wordList.append(key)

   command = 5
   while command > 3:
      command = int(input(terminalUI))

   prompt += wordList[command]
