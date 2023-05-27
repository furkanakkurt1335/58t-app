import os, json, re

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(THIS_DIR, '..', 'data')
corpora_l = ['coca', 'now']
files = [os.path.join(DATA_DIR, i + '.json') for i in corpora_l]
merged_l = []
for file in files:
    with open(file, 'r') as f:
        body_l = json.load(f)
        print(len(body_l))
    merged_l.extend(body_l)
print('Corpus loaded.')
print('Total lines:', len(merged_l))

with open(os.path.join(DATA_DIR, 'merged.json'), 'w') as f:
    json.dump(merged_l, f, indent=4, ensure_ascii=False)
print('JSON dumped.')
