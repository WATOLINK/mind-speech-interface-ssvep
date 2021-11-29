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

# while 1:
#    print(prompt)
#    res = openai.Completion.create(engine="curie", max_tokens=1, temperature=1, n = 1, prompt = prompt, logprobs=3)
#    wordDict = res["choices"][0]["logprobs"]["top_logprobs"][0]
#    wordList = []
#    terminalUI = ""
   
#    for index, key in enumerate(wordDict):
#       terminalUI = terminalUI + str(index) + ": " + key + "\n"
#       wordList.append(key)

#    command = 5
#    while command > 3:
#       command = int(input(terminalUI))

#    prompt += wordList[command]
# stopCondition = [".", "!", "\n", ","]
# print(prompt)
# res = openai.Completion.create(engine="curie", max_tokens=10, temperature=0.1, n = 3, prompt = prompt, stop = stopCondition)
# print(res)

