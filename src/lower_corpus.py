import os, json

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(THIS_DIR, '..', 'data')
corpus_path = os.path.join(DATA_DIR, 'coca-samples-text.json')
with open(corpus_path, 'r') as f:
    body_d = json.load(f)
print('Corpus loaded.')

for key in body_d.keys():
    body_d[key] = body_d[key].lower()

with open(os.path.join(DATA_DIR, 'coca-samples-text.json'), 'w') as f:
    json.dump(body_d, f, indent=4, ensure_ascii=False)
print('JSON dumped.')