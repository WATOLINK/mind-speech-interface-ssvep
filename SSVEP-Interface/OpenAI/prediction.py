import os
import openai
from dotenv import load_dotenv

class OpenAI():

    def __init__(self, engine="curie", stop_condition=[".", "!", "\n", ","]):
        '''Initializes OpenAI with provided parameters, leave as empty for default

            If missing API Key, contact Jackie on Discord
        '''
        load_dotenv()
        OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
        openai.api_key = OPENAI_API_KEY
        self.engine = engine
        self.stop_condition = stop_condition

    def predictWords(self, prompt, num_results=3):
        '''Generates up to #num_results predicted word for the given prompt'''
        res = openai.Completion.create(engine=self.engine, max_tokens=1, temperature=0.8, n = num_results, prompt = prompt)
        wordDict = res["choices"]
        wordList = []
        print(res)
        for index, key in enumerate(wordDict):
            wordList.append(wordDict[index]["text"])
        wordList = list(dict.fromkeys(wordList))
        return wordList

    def predictedSentences(self, prompt, num_results=3):
        '''Generates up to #num_results unique sentences as a response to given prompt'''
        res = openai.Completion.create(engine=self.engine, max_tokens=50, temperature=1, n = num_results, prompt = prompt, stop = ["\n", ".", "!"])
        wordDict = res["choices"]
        wordList = []
        print(res)
        for index, key in enumerate(wordDict):
            wordList.append(wordDict[index]["text"])
        
        return wordList
