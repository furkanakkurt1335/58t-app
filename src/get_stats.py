import os, json
from transformers import BertTokenizer, BertModel, AutoConfig

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(THIS_DIR, '..', 'data')
corpus_path = os.path.join(DATA_DIR, 'cleaned.json')
with open(corpus_path, 'r') as f:
    body_d = json.load(f)
print('Corpus loaded. Total lines:', len(body_d))

config = AutoConfig.from_pretrained('bert-base-uncased', output_hidden_states=True)
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', config=config)

len_d = {'token': {'max': 0, 'bigger': 0}, 'body': {'max': 0}}
bigger_count = 0
for id_t, body in body_d.items():
    body_len = len(body)
    if body_len > len_d['body']['max']:
        len_d['body']['max'] = body_len
    tokens = tokenizer.tokenize(body)
    token_len = len(tokens)
    if token_len > len_d['token']['max']:
        len_d['token']['max'] = token_len
    if token_len > 512:
        len_d['token']['bigger'] += 1
    if int(id_t) % 100 == 0:
        print(f'{id_t} bodies processed.')
print(len_d)