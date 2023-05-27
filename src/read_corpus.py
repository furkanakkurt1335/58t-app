import os

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(THIS_DIR, '..', 'data')
corpus_path = os.path.join(DATA_DIR, 'coca-samples-text')
files = os.listdir(corpus_path)
corpus_d = {}
print('Loading corpus...')
for file in files:
    with open(os.path.join(corpus_path, file), 'r') as f:
        corpus_d[file] = f.read()
print('Corpus loaded.')

total_tokens_len = 0
for key in corpus_d.keys():
    text = corpus_d[key]
    tokens = text.split(' ')
    tokens_len = len(tokens)
    total_tokens_len += tokens_len
    print(key, tokens_len)
print('Total tokens length:', total_tokens_len)