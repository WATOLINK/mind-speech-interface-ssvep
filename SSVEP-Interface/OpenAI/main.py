from prediction import OpenAI

o = OpenAI()

prompt = "Question: " + "How did you like the movie last night" + "?\nAnswer: I thought it was Great. I really liked how the main character"

res = o.predictWords(prompt, num_results=100)

print(res)
