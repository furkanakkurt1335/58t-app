import os, json

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(THIS_FOLDER, '../data')

entry_path = os.path.join(data_path, 'sense_count_d.json')
with open(entry_path, 'r') as f:
    entry_d = json.load(f)
words = list(entry_d.keys())

cluster_path = os.path.join(data_path, 'cluster_min_distances.json')
with open(cluster_path) as f:
    cluster_d = json.load(f)

dist_l = [(cluster_d[word], word) for word in cluster_d]
dist_l.sort()
for t in dist_l[:10]:
    dist, word = t
    print('{} {:.4f}'.format(word, dist))
# economy 0.0377
# standard 0.0378
# number 0.0394
# story 0.0415
# monument 0.0420
# culture 0.0423
# vote 0.0423
# pie 0.0424
# approach 0.0427
# move 0.0428