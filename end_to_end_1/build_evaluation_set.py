import os
import shutil
import argparse


KEPT_EXT = ['PNG', 'SEMANTIC']

parser = argparse.ArgumentParser(description='Clean primus data')
parser.add_argument('-primus', dest='primus', type=str, required=True, help='Path to the primus dataset.')
parser.add_argument('-output', dest='output', type=str, required=True, help='Path to the output folder.')
parser.add_argument('-samples_count', dest='samples_cnt', type=int, default=-1, help='Number of samples.')
args = parser.parse_args()

cnt = 0

for dir in os.listdir(args.primus):
    dir_path = os.path.join(args.primus, dir)
    for filename in os.listdir(dir_path):
        outfolder = os.path.join(args.output, dir)
        print(outfolder)
        try: 
            os.mkdir(outfolder) 
        except OSError as error:
            pass

        if filename.split('.')[-1].upper() in KEPT_EXT and not filename.startswith('.'):
            filepath = os.path.join(dir_path, filename)
            outpath = os.path.join(outfolder, filename)
            shutil.copy(filepath, outpath)

    cnt += 1
    if args.samples_cnt > -1 and cnt == args.samples_cnt:
        break
