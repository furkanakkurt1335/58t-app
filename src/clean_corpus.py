import os, json, re

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(THIS_DIR, '..', 'data')
corpus_path = os.path.join(DATA_DIR, 'merged.json')
with open(corpus_path, 'r') as f:
    body_l = json.load(f)
print('Corpus loaded.')

tag_l = ['p', 't', 'h', 'br']
tag_pattern = re.compile(r'</?([^ ]*?)>')
for i, body in enumerate(body_l):
    tag_search = tag_pattern.search(body)
    if tag_search:
        tag_s = tag_search.group(1)
        if tag_s in tag_l:
            body_l[i] = body.replace(tag_search.group(0), '')

print('Writing to file...')
with open(os.path.join(DATA_DIR, 'cleaned.json'), 'w') as f:
    json.dump(body_l, f, indent=4, ensure_ascii=False)
print('Done.')