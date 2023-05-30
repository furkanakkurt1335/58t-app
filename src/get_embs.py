import os, json, torch, pickle
from transformers import BertTokenizer, BertModel
import numpy as np

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
print('Total lines:', len(id_l))
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
            # sum last 4 layers
            token_representations = np.array([outputs.hidden_states[i][0, idx, :].detach().cpu().numpy() for i in range(9, 13)])
            repr = np.sum(token_representations, axis=0)
            rounded_repr = np.round(repr, 4)
            repr_d[token].append({'body_id': id_t, 'representation': repr})
    
    if i % 100 == 0:
        print('Line:', i)
        print('Remaining:', len(id_l) - i)

repr_pkl_path = os.path.join(DATA_DIR, 'repr_d-rounded.pkl')
with open(repr_pkl_path, 'wb') as f:
    pickle.dump(repr_d, f)
    print('Pickle dumped')