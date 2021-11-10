import pandas as pd
import spacy
import os

CORPUS_PATH = './utils/corpus-v2.txt'


def prompt_conditions(prompt):
    return True


def process_corpus():
    """ Text parameter should be string to extract and generate prompts for """
    curated_prompts = []

    if (not os.path.isfile(CORPUS_PATH)):
        print("creating corpus...")
        nlp = spacy.load('en_core_web_sm')

        df = pd.read_csv("./utils/dataset.csv", nrows=600)

        text = ' '.join(df['text'].tolist())
        doc = nlp(text)

        with open(CORPUS_PATH, 'w', encoding="utf-8") as f:
            for token in doc.noun_chunks:
                prompt = token.text
                if prompt_conditions(prompt=prompt):
                    f.write("%s\n" % prompt)
                    curated_prompts.append(prompt)
    else:
        print("loading corpus...")
        with open(CORPUS_PATH, 'r', encoding="utf-8") as f:
            curated_prompts = f.read().splitlines()

    return curated_prompts

    # prompts_count = Counter(curated_prompts)

    # for item in prompts_count.most_common():
    #     data.append([item[0], item[1]])
    #     # data['ngram'] = item[0]
    #     # data['freq'] = item[1]

    # return pd.DataFrame(data, columns=['ngram', 'freq'])


# prompts = process_corpus()
# print(prompts)
