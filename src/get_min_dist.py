import os, json

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(THIS_FOLDER, '../data')
cluster_path = os.path.join(data_path, 'cluster_distances.json')
with open(cluster_path) as f:
    cluster_d = json.load(f)

min_dist_l = [(cluster_d[word]['min'], word) for word in cluster_d]
min_dist_l.sort()
min_dist = min_dist_l[0][0]
print(min_dist_l[:10])
max_dist_l = [(cluster_d[word]['max'], word) for word in cluster_d]
max_dist_l.sort()
min_max_dist = max_dist_l[0][0]
print(max_dist_l[:10])

print('Min distance:', min_dist)
print('Min max distance:', min_max_dist)
# for t in dist_l[:10]:
#     dist, word = t
#     print('{} {:.4f}'.format(word, dist))
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

with open(os.path.join(data_path, 'min-dist.json'), 'w') as f:
    json.dump({'min': min_dist, 'min_max': min_max_dist}, f, indent=4)