import os, json, psutil
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_distances

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(THIS_FOLDER, '../data')

entry_path = os.path.join(data_path, 'sense_count_d.json')
with open(entry_path, 'r') as f:
    entry_d = json.load(f)
words = list(entry_d.keys())

repr_d_path = os.path.join(data_path, 'repr_d-rounded')
repr_files = [i for i in os.listdir(repr_d_path) if i.endswith('.json')]

cluster_path = os.path.join(data_path, 'cluster_min_distances.json')
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
    kmeans = KMeans(n_clusters=entry_d[word], random_state=0, n_init="auto").fit(data[word])
    distances = cosine_distances(kmeans.cluster_centers_)
    min_distance = 1
    for distance in distances:
        for el in distance:
            if el != 0 and el < min_distance:
                min_distance = el
    print('Min distance:', min_distance)
    cluster_d[word] = min_distance
    with open(cluster_path, 'w') as f:
        json.dump(cluster_d, f)