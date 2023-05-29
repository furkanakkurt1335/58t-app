from transformers import BertTokenizer, BertModel
import torch
from scipy.spatial.distance import cosine

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load the BERT tokenizer and model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased', output_hidden_states=True)

sentences = ['The river bank was full of dead fishes. I was afraid to swim there. The putrid smell emanating from the dead fish was overwhelming, and it made me feel sick to my stomach. I wondered what could have caused such a catastrophic event, as I had never seen so many dead fish in one place before. Perhaps there had been a chemical spill or some other environmental disaster that had contaminated the river. Whatever the cause, it was clear that the water was not safe to swim in, and I decided to find another place to cool off on this hot summer day.', 'I went to the bank to withdraw my money. The bank was closed since it was Sunday. As I approached the bank, I noticed that the usual hustle and bustle of people coming and going was notably absent. It was then that I realized that it was Sunday, and the bank was closed. I had completely forgotten about the limited hours of operation on weekends, and the disappointment was palpable. I needed to withdraw my money urgently to pay for some bills, and I didn\'t know what to do next. I made a mental note to check the bank\'s hours of operation in the future to avoid similar situations and decided to explore other options, such as online banking or using an ATM.']
word = 'bank'
repr_l = []
# Tokenize the input sequence
for i, sentence in enumerate(sentences):
    tokens = tokenizer.tokenize(sentence)
    input_ids = torch.tensor(tokenizer.convert_tokens_to_ids(tokens)).unsqueeze(0)
    input_ids = input_ids.to(torch.long).to(device)
    attention_mask = torch.ones_like(input_ids)
    attention_mask = attention_mask.to(torch.long).to(device)

    # Feed the inputs into BERT's transformer network
    outputs = model(input_ids=input_ids, attention_mask=attention_mask)

    # Retrieve the contextualized representations from the model's hidden states (the last 4 layers) and average them
    tokens_temp = tokens.copy()
    for order in range(tokens.count(word)):
        token_index = tokens_temp.index(word)
        token_representations = [i[0][token_index] for i in outputs.hidden_states[-4:]]
        concat_repr = torch.cat(token_representations, dim=0)
        repr_l.append({'sentence': ' '.join(tokens_temp), 'representation': concat_repr.detach().numpy()})
        tokens_temp[token_index] = 'X'

out_l = []
for i, repr1 in enumerate(repr_l):
    for j, repr2 in enumerate(repr_l[i+1:]):
        dist = cosine(repr1['representation'], repr2['representation'])
        print('Sentence 1:', repr1['sentence'])
        print('Sentence 2:', repr2['sentence'])
        print('Distance:', dist)
        print()
