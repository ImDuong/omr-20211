import os
import glob
import argparse
from tqdm import tqdm

parser = argparse.ArgumentParser(description='Evaluate the prediction result.')
parser.add_argument('-evaluate', dest='eval', type=str, required=True, help='Path to the evaluation set')
args = parser.parse_args()

def get_symbols(file_path):
    with open(file_path, 'r') as f:
        raw = f.read()
        symbols = [s.rstrip() for s in raw.split('\t') if s.rstrip()]
        return symbols

def filter_symbols(symbols):
    filtered_symbols = []
    for s in symbols:
        if 'note' in s:
            filtered_symbols.append(s)

    return filtered_symbols       

def compare(label_syms, pred_syms, tolerance=2):
    matches = 0
    total = 0

    for i in range(len(label_syms)):
        try: 
            total += 1
            if pred_syms[i] == label_syms[i]:
                matches += 1
            else:
                    for tol in range(tolerance):
                        if pred_sem[i - tol] == label_syms[i]:
                            matches += 1
                            break
                        elif pred_sem[i + tol] == label_syms[i]:
                            matches += 1
                            break
        except:
            pass

    return (matches, total)
        
matches = 0
total = 0 
sample_cnt = 0

for sample in tqdm(os.listdir(args.eval)):
    sample_path = os.path.join(args.eval, sample)
    label_sem = glob.glob(f'{sample_path}/{sample}.semantic')[0]
    pred_sem = glob.glob(f'{sample_path}/{sample}_pred.semantic')[0]

    label_symbols = get_symbols(label_sem)
    pred_symbols = get_symbols(pred_sem)
    
    label_symbols = filter_symbols(label_symbols)
    pred_symbols = filter_symbols(pred_symbols)

    m, t = compare(label_symbols, pred_symbols)

    sample_cnt += 1
    matches += m
    total += t

print(f'Evaluation result: Model return the symbol error rate of {round(matches / total * 100, 2)}, evaluated on {sample_cnt} samples')