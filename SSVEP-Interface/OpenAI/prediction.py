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
        res = openai.Completion.create(engine=self.engine, max_tokens=1, temperature=1, n = 1, prompt = prompt, logprobs=num_results)
        wordDict = res["choices"][0]["logprobs"]["top_logprobs"][0]
        wordList = []
    
        for index, key in enumerate(wordDict):
            wordList.append(key)
        
        return wordList

    def predictedSentences(self, prompt, num_results=3):
        '''Generates up to #num_results unique sentences as a response to given prompt'''
        sentenceList = []
        temperature = 0.1
        while len(sentenceList) < num_results:
            res = openai.Completion.create(engine=self.engine, max_tokens=10, temperature=0.1, n = 3, prompt = prompt, stop = self.stop_condition)
            for key in res["choices"]:
                if key["text"] not in sentenceList:
                    sentenceList.append(key["text"])
            temperature += 0.2
        return sentenceList