import os
import argparse
from tqdm import tqdm


parser = argparse.ArgumentParser(description='Clean primus data')
parser.add_argument('-primus', dest='primus', type=str, required=True, help='Path to the primus dataset.')
args = parser.parse_args()

DATA_PATH = args.primus
KEPT_EXTENSIONS = ['png', 'semantic', 'agnostic']

for dir in tqdm(os.listdir(DATA_PATH)):
    dir_path = os.path.join(DATA_PATH, dir)
    for filename in os.listdir(dir_path):
        filepath = os.path.join(dir_path, filename)
        if filename.startswith('.') or filename.split('.')[-1] not in KEPT_EXTENSIONS:
            os.remove(filepath)