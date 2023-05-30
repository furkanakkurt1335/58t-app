import os, json, argparse
import numpy as np
from sklearn.metrics.pairwise import cosine_distances
from sklearn.cluster import AgglomerativeClustering

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(THIS_FOLDER, '../data')

parser = argparse.ArgumentParser(description='Cluster words')
parser.add_argument('--type', type=str, default='kmeans', help='Type of clustering', required=True)
args = parser.parse_args()
cluster_type = args.type
cluster_path = ''
min_dist = 0
min_max_dist = 0
max_dist = 1
if cluster_type == 'n_clusters':
    cluster_path = os.path.join(data_path, 'cluster_distances.json')
elif cluster_type == 'distance':
    cluster_path = os.path.join(data_path, 'cluster_counts.json')
    min_dist_path = os.path.join(data_path, 'min-dist.json')
    with open(min_dist_path, 'r') as f:
        min_dist_d = json.load(f)
    min_dist = min_dist_d['min']
    min_max_dist = min_dist_d['min_max']
    max_dist = min_dist_d['max']

entry_path = os.path.join(data_path, 'sense_count_d.json')
with open(entry_path, 'r') as f:
    entry_d = json.load(f)
words = list(entry_d.keys())

repr_d_path = os.path.join(data_path, 'repr_d-rounded')
repr_files = [i for i in os.listdir(repr_d_path) if i.endswith('.json')]

if os.path.exists(cluster_path):
    with open(cluster_path) as f:
        cluster_d = json.load(f)
else:
    cluster_d = {}
data = {}
for i, repr_file in enumerate(repr_files):
    print('File:', i)
    with open(os.path.join(repr_d_path, repr_file)) as f:
        d_t = json.load(f)
    for word in d_t:
        if word not in data:
            data[word] = []
        data[word].extend(d_t[word])

for word in words:
    if word in cluster_d or not data[word] or entry_d[word] < 1:
        continue
    print('Word:', word)
    if cluster_type == 'n_clusters':
        arr = np.array(data[word])
        agglo = AgglomerativeClustering(n_clusters=entry_d[word], metric='cosine', linkage='average', compute_distances=True).fit(arr)
        labels = agglo.labels_
        d = {i: np.array([]) for i in range(agglo.n_clusters_)}
        for i in set(labels):
            d[i] = arr[labels == i]
        center_d = {i: np.mean(d[i], axis=0) for i in d}
        distances = cosine_distances(np.array(list(center_d.values())))
        flat_arr = np.triu(distances).flatten()
        flat_arr = np.delete(flat_arr, np.where(flat_arr == 0))
        if len(flat_arr) < 1:
            continue
        min_distance = np.min(flat_arr)
        print('Min distance:', min_distance)
        max_distance = np.max(flat_arr)
        print('Max distance:', max_distance)
        mean_distance = np.mean(flat_arr)
        print('Mean distance:', mean_distance)
        cluster_d[word] = {'min': min_distance, 'max': max_distance, 'mean': mean_distance}
    elif cluster_type == 'distance':
        agglo = AgglomerativeClustering(distance_threshold=min_dist, n_clusters=None, metric='cosine', linkage='average').fit(data[word])
        cluster_count = agglo.n_clusters_
        print('Cluster count:', cluster_count)
        cluster_d[word] = cluster_count
    with open(cluster_path, 'w') as f:
        json.dump(cluster_d, f)