import os, json, re, argparse

parser = argparse.ArgumentParser()
parser.add_argument('--corpus', type=str, help='Corpus name')
args = parser.parse_args()

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(THIS_DIR, '..', 'data')
if args.corpus == 'now':
    corpus_path = os.path.join(DATA_DIR, 'now')
elif args.corpus == 'coca':
    corpus_path = os.path.join(DATA_DIR, 'coca')
files = os.listdir(corpus_path)
corpus_d = {}
print('Loading corpus...')
for file in files:
    with open(os.path.join(corpus_path, file), 'r') as f:
        corpus_d[file] = f.read()
print('Corpus loaded.')

body_l = []
line_start_pattern = re.compile(r'^@@\w*')
for key, content in corpus_d.items():
    for line in content.split('\n'):
        line_start_search = line_start_pattern.search(line)
        if line_start_search:
            line_start = line_start_search.group()
            line = line[line_start_search.end():].strip()
            if len(line) == 0:
                continue
            body_l.append(line.strip())

print('Total lines:', len(body_l))

with open(os.path.join(DATA_DIR, '{}.json'.format(args.corpus)), 'w') as f:
    json.dump(body_l, f, indent=4, ensure_ascii=False)
print('JSON dumped.')
