import os, json, re

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

body_l = []
line_start_pattern = re.compile(r'^@@\d+')
for key, content in corpus_d.items():
    for line in content.split('\n'):
        line = line.strip()
        if len(line) == 0:
            continue
        body_l.append(line)

print('Total lines:', len(body_l))

with open(os.path.join(DATA_DIR, 'coca-samples-text.json'), 'w') as f:
    json.dump(body_l, f, indent=4, ensure_ascii=False)
print('JSON dumped.')
