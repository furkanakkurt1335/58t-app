import os, json
from transformers import BertTokenizer, BertModel
import torch

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(THIS_DIR, '..', 'data')
corpus_path = os.path.join(DATA_DIR, 'cleaned.json')
with open(corpus_path, 'r') as f:
    body_d = json.load(f)
print('Corpus loaded. Total lines:', len(body_d))
entry_path = os.path.join(DATA_DIR, 'sense_count_d.json')
with open(entry_path, 'r') as f:
    entry_d = json.load(f)
words = list(entry_d.keys())

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model_name = 'bert-base-uncased'
print('Loading model {}...'.format(model_name))
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name, output_hidden_states=True)
model = model.to(device)
print('Model {} loaded.'.format(model_name))

id_l = list(body_d.keys())
repr_d = {word: [] for word in words}
for i, id_t in enumerate(id_l):
    body = body_d[id_t]
    tokens = tokenizer.tokenize(body)
    tokens = tokens[:512]
    input_ids = torch.tensor(tokenizer.convert_tokens_to_ids(tokens)).unsqueeze(0).to(device)
    attention_mask = torch.ones_like(input_ids).to(device)
    outputs = model(input_ids=input_ids, attention_mask=attention_mask)

    for idx, token in enumerate(tokens):
        if token in words:
            token_representations = [i[0][idx] for i in outputs.hidden_states[-4:]]
            concat_repr = torch.cat(token_representations, dim=0)
            repr_d[token].append({'body_id': id_t, 'representation': concat_repr.detach().cpu().numpy().tolist()})
    
    if i % 1000 == 0:
        repr_path = os.path.join(DATA_DIR, 'repr_d-{}.json'.format(i))
        with open(repr_path, 'w') as f:
            json.dump(repr_d, f)
        print('Representations saved at {}.'.format(repr_path))
        repr_d = {word: [] for word in words}

repr_path = os.path.join(DATA_DIR, 'repr_d-last.json')
with open(repr_path, 'w') as f:
    json.dump(repr_d, f)
print('Representations saved at {}.'.format(repr_path))
