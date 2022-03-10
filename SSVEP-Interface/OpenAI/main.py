from prediction import OpenAI

o = OpenAI()

prompt = "Question: " + "Who is your favourite Superhero" + "?\nAnswer:"

res = o.predictedSentences(prompt, num_results=5)

print(res)
