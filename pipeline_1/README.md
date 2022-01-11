# How to run

Granted that the primus dataset has been downloaded from https://grfia.dlsi.ua.es/primus/

# Predict a single file

> Example: !python predict_single.py -image <path of the image file> -out <output location> -model <path of the model> -vocabulary <path to the vocabulary>

# Predict multiple files

## Build the evaluation set

> Example: 'python build_evaluation_set.py -primus <path of primus dataset> -output /content/eval_set -samples_count 150'

## Run the main file to generate predictions

> for example `python predict_multi.py -evaluate <path of evaluation set> -model <path of the model> -vocabulary <path to the vocabulary>

## The output can be found in the evaluation set with '_pred' surfix