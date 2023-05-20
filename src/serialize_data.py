import os, argparse, json
import pandas as pd

parser = argparse.ArgumentParser(description='Serialize data')
parser.add_argument('--file', type=str, default='data', help='data filepath')
parser.add_argument('--format', type=str, help='data format')
parser.add_argument('--sheet', type=str, help='data sheet')
parser.add_argument('--source', type=str, help='data source')
args = parser.parse_args()
data_filepath = args.file
data_format = args.format
data_source = args.source

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(THIS_DIR, '..', 'data')
data_filename = os.path.basename(data_filepath)
output_path = os.path.join(DATA_DIR, f'{data_filename}.json')

if data_format == 'txt':
    with open(data_filepath, 'r') as f:
        entry_l = f.read().split('\n')
    entry_d = {'entries': entry_l, 'source': data_source}

elif data_format == 'xlsx':
    sheet_name = args.sheet
    entry_l = []
    df = pd.read_excel(data_filepath, sheet_name=sheet_name)
    for i in range(len(df)):
        lemma_t = df.iloc[i]['lemma']
        pos_t = df.iloc[i]['PoS']
        if pos_t == 'n':
            entry_l.append(lemma_t)
    entry_d = {'entries': entry_l, 'source': data_source}

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(entry_d, f, indent=2, ensure_ascii=False)
