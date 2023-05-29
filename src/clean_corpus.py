import os, json, re

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(THIS_DIR, '..', 'data')
corpus_path = os.path.join(DATA_DIR, 'merged.json')
with open(corpus_path, 'r') as f:
    body_d = json.load(f)
print('Corpus loaded.')

tag_l = ['p', 't', 'h', 'br']
tag_pattern = re.compile(r'</?([^ ]*?)>')
new_body_d = {}
for id_t, body in body_d.items():
    tag_search = tag_pattern.search(body)
    if tag_search:
        tag_s = tag_search.group(1)
        if tag_s in tag_l:
            body = body.replace(tag_search.group(0), '')
        while '  ' in body:
            body = body.replace('  ', ' ')
        body = body.strip()
        if body:
            new_body_d[id_t] = body

print('Writing to file...')
with open(os.path.join(DATA_DIR, 'cleaned.json'), 'w') as f:
    json.dump(new_body_d, f, indent=4, ensure_ascii=False)
print('Done.')