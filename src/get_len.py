import os, json

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(THIS_DIR, '..', 'data')
freq_path = os.path.join(DATA_DIR, 'freq-nouns-coca.json')
with open(freq_path, 'r') as f:
    freq_d = json.load(f)

print('Freq loaded. Total words:', len(freq_d['entries']))