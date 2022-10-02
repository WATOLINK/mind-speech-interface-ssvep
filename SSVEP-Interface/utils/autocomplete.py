CORPUS_PATH = 'SSVEP-Interface/utils/corpus-v2.txt'


def process_corpus():
    ''' Text parameter should be string to extract and generate prompts for '''
    curated_prompts = []

    print("loading corpus...")
    with open(CORPUS_PATH, 'r', encoding="utf-8") as f:
        curated_prompts = f.read().splitlines()

    return curated_prompts
