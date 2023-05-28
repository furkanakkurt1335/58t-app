import os, json

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(THIS_DIR, '..', 'data')
corpus_path = os.path.join(DATA_DIR, 'merged.json')
with open(corpus_path, 'r') as f:
    body_l = json.load(f)
print('Corpus loaded.')

word = 'inception'
count = 0
for i, body in enumerate(body_l):
    if word in body:
        count += 1
    if body.count(word) > 1:
        print(body)

print('Total lines:', len(body_l))
print('Total lines with "{}": {}'.format(word, count))
