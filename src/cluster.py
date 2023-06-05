import os, json, argparse, pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_distances
from sklearn.cluster import AgglomerativeClustering
from matplotlib import pyplot as plt
from sklearn.manifold import TSNE

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(THIS_FOLDER, '../data')

parser = argparse.ArgumentParser(description='Cluster words')
parser.add_argument('-t', '--type', type=str, default='n_clusters', help='Type of clustering', required=True)
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

repr_pkl_dir = os.path.join(data_path, 'repr_d-rounded')
data = {}
pkl_files = os.listdir(repr_pkl_dir)
for pkl_file in pkl_files:
    with open(os.path.join(repr_pkl_dir, pkl_file), 'rb') as f:
        data.update(pickle.load(f))
        print('Pickle loaded')

data_len = len(data)
print('Data length:', data_len)

if os.path.exists(cluster_path):
    with open(cluster_path) as f:
        cluster_d = json.load(f)
else:
    cluster_d = {}

words = ['people']
for word in words:
    # if word in cluster_d or not data[word] or entry_d[word] < 1:
    #     continue
    print('Word:', word)
    arr = np.array([data[word][i]['representation'] for i in range(len(data[word]))])
    if cluster_type == 'n_clusters':
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
        min_distance = np.min(flat_arr).item()
        print('Min distance:', min_distance)
        max_distance = np.max(flat_arr).item()
        print('Max distance:', max_distance)
        mean_distance = np.mean(flat_arr).item()
        print('Mean distance:', mean_distance)
        cluster_d[word] = {'min': min_distance, 'max': max_distance, 'mean': mean_distance}
    elif cluster_type == 'distance':
        print('Calculating clusters')
        agglo = AgglomerativeClustering(distance_threshold=min_dist, n_clusters=None, metric='cosine', linkage='average').fit(arr)
        labels = agglo.labels_
        cluster_count = agglo.n_clusters_
        print('Cluster count:', cluster_count)
        cluster_d[word] = cluster_count
    print('Plotting')
    X_embedded = TSNE(n_components=2, metric='cosine').fit_transform(arr)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(X_embedded[:, 0], X_embedded[:, 1], c=labels, cmap='tab20')
    plt.title(word)
    im_dir = os.path.join(data_path, 'cluster-plot_tsne')
    if not os.path.exists(im_dir):
        os.mkdir(im_dir)
    plt.savefig(os.path.join(im_dir, '{}-{}.png'.format(word, cluster_type)))
    with open(cluster_path, 'w') as f:
        json.dump(cluster_d, f)