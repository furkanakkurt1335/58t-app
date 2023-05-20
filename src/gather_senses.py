import requests, json, os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
data_folder = os.path.join(THIS_FOLDER, '..', 'data')

creds_file = os.path.join(THIS_FOLDER, 'creds.json')
if not os.path.exists(creds_file):
    raise Exception('Please create a creds.json file with your Merriam-Webster API key.')
with open(creds_file, 'r') as f:
    data = json.load(f)
    if 'api_key' not in data:
        raise Exception('Please add your Merriam-Webster API key to the creds.json file.')
    api_key = data['api_key']

noun_file = os.path.join(data_folder, '1525-freq-nouns.json')
with open(noun_file, 'r') as f:
    noun_l = json.load(f)['entries']
url = 'https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={api_key}'

sense_path = os.path.join(data_folder, 'sense_d.json')
if os.path.exists(sense_path):
    with open(sense_path, 'r') as f:
        sense_d = json.load(f)
else:
    sense_d = {}
for noun in noun_l:
    if noun in sense_d.keys():
        continue
    req_url = url.format(word=noun, api_key=api_key)
    r = requests.get(req_url)
    if r.status_code == 200:
        sense_d[noun] = r.json()
    break

with open(os.path.join(data_folder, 'sense_d.json'), 'w') as f:
    json.dump(sense_d, f, indent=4, ensure_ascii=False)