from transformers import BertTokenizer, BertModel, AutoConfig
import torch
from scipy.spatial.distance import cosine

# Load the BERT tokenizer and model
config = AutoConfig.from_pretrained('bert-base-uncased', output_hidden_states=True)
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', config=config)
model = BertModel.from_pretrained('bert-base-uncased', config=config)

sentences = ['Count Ugolino has been imprisoned with his sons and grandsons to starve to death.', 'I have counted the number of times.', 'The count is in the millions.', 'The Count of Monte Cristo is a novel by Alexandre Dumas.']
words = ['count', 'counted', 'count', 'count']
repr_l = []
# Tokenize the input sequence
for i, sentence in enumerate(sentences):
    tokens = tokenizer.tokenize(sentence)
    input_ids = torch.tensor(tokenizer.convert_tokens_to_ids(tokens)).unsqueeze(0)
    attention_mask = torch.ones_like(input_ids)

    # Feed the inputs into BERT's transformer network
    outputs = model(input_ids=input_ids, attention_mask=attention_mask)

    # Retrieve the contextualized representations from the model's hidden states (the last 4 layers) and average them
    token_index = tokens.index(words[i])
    token_representation = outputs.hidden_states[-1][0][token_index]
    for j in range(2, 5):
        token_representation += outputs.hidden_states[-j][0][token_index]
    token_representation /= 4
    repr_l.append({'sentence': sentence, 'token': tokens[token_index], 'representation': token_representation.detach().numpy()})

out_l = []
for i, repr1 in enumerate(repr_l):
    for j, repr2 in enumerate(repr_l[i+1:]):
        dist = cosine(repr1['representation'], repr2['representation'])
        out_l.append({'sent1': repr1['sentence'], 'sent2': repr2['sentence'], 'dist': dist})
out_l.sort(key=lambda x: x['dist'])
for out in out_l:
    print('{dist:.4f}: "{sent1}" and "{sent2}"'.format(sent1=out['sent1'], sent2=out['sent2'], dist=out['dist']))
