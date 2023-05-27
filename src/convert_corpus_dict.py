import os, json, re, random

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(THIS_DIR, '..', 'data')
corpus_path = os.path.join(DATA_DIR, 'coca-samples-text.json')
with open(corpus_path, 'r') as f:
    body_l = json.load(f)
print('Corpus loaded.')

line_start_pattern = re.compile(r'^@@\w*')
body_d = {}
for i, body in enumerate(body_l):
    line = body.strip()
    if len(line) == 0:
        continue
    tokens = line.split(' ')
    line_start_search = line_start_pattern.search(line)
    if line_start_search:
        line_start = line_start_search.group()
        line = line[line_start_search.end():].strip()
        if len(line) == 0:
            continue
        body_d[i] = line

with open(os.path.join(DATA_DIR, 'coca-samples-text.json'), 'w') as f:
    json.dump(body_d, f, indent=4, ensure_ascii=False)
print('JSON dumped.')
