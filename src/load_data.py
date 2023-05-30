import os, psutil, pickle

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(THIS_FOLDER, '../data')
repr_pkl_path = os.path.join(data_path, 'repr_d-rounded.pkl')
with open(repr_pkl_path, 'rb') as f:
    data = pickle.load(f)
print(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)
