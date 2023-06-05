import os, json, pickle

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(THIS_DIR, '../data')
pkl_path = os.path.join(DATA_DIR, 'repr_d-rounded.pkl')
rounded_dir = os.path.join(DATA_DIR, 'repr_d-rounded')
with open(pkl_path, 'rb') as f:
    data = pickle.load(f)
    print('Pickle loaded')

words = list(data.keys())
words_len = len(words)

# split data into 10 parts
split_count = 10
for i in range(split_count):
    new_data = {}
    word_batch = words[i * words_len // split_count: (i + 1) * words_len // split_count]
    for word in word_batch:
        new_data[word] = data[word]
    new_pkl_path = os.path.join(rounded_dir, 'repr_d-rounded-{}.pkl'.format(i))
    with open(new_pkl_path, 'wb') as f:
        pickle.dump(new_data, f)
        print('Pickle dumped')
