import os, argparse, json

parser = argparse.ArgumentParser(description='Serialize data')
parser.add_argument('--data', type=str, default='data', help='data directory')
args = parser.parse_args()
data_file = args.data

with open(data_file, 'r') as f:
    entry_l = f.read().split('\n')

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(THIS_DIR, '..', 'data')

entry_d = {'entries': entry_l}

with open(os.path.join(DATA_DIR, 'entries.json'), 'w') as f:
    json.dump(entry_d, f, indent=2)