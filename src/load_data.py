import os, json, psutil

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(THIS_FOLDER, '../data')
repr_d_path = os.path.join(data_path, 'repr_d-rounded')
repr_files = [i for i in os.listdir(repr_d_path) if i.endswith('.json')]
data = {}
for file in repr_files:
    with open(os.path.join(repr_d_path, file)) as f:
        d_t = json.load(f)
    print(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)
    for word in d_t:
        if word not in data:
            data[word] = []
        data[word].extend(d_t[word])
