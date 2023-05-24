import json, os, re

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
data_folder = os.path.join(THIS_FOLDER, '..', 'data')
sense_path = os.path.join(data_folder, 'sense_d.json')
with open(sense_path, 'r') as f:
    sense_d = json.load(f)

count_d = {}
nouns = list(sense_d.keys())
for i, noun in enumerate(nouns):
    data = sense_d[noun]
    id_pattern = f'{noun}:.+'
    sense_count = 0
    for j, sense in enumerate(data):
        if not isinstance(sense, dict): # word is not found in the dictionary
            continue
        id_t = sense['meta']['id'].lower()
        form = sense['hwi']['hw'].replace('*', '')
        id_match = re.match(id_pattern, id_t)
        if noun == 're-election':
            print(noun.replace('-', '') in [i.lower() for i in sense['meta']['stems']])
        if id_match or noun == form or noun in [i.lower() for i in sense['meta']['stems']] or noun.replace('-', '') in [i.lower() for i in sense['meta']['stems']]:
            if 'fl' not in sense.keys():
                if form == noun:
                    sense_count += 1
            else:
                for i in sense['def']:
                    sense_count += len(i['sseq'])
    count_d[noun] = sense_count

count_path = os.path.join(data_folder, 'sense_count_d.json')
with open(count_path, 'w') as f:
    json.dump(count_d, f, indent=2)