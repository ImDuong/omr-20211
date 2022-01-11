## How to run
Granted that the primus dataset has been downloaded from https://grfia.dlsi.ua.es/primus/

To format the output to midi, a semantic to midi converter is needed

- the primus converter can be found at https://grfia.dlsi.ua.es/primus/

## Train model

> python ctc_training.py -semantic -corpus <path to primus> -set Data/train.txt -vocabulary Data/vocabulary_semantic.txt  -save_model ./trained_semantic_model

## Prediction

1. Predict a single file
> Example: !python predict_single.py -image <path of the image file> -out <output location> -model <path of the model> -vocabulary <path to the vocabulary>


2. Predict multiple files
    a. Build the evaluation set
> Example: 'python build_evaluation_set.py -primus <path of primus dataset> -output /content/eval_set -samples_count 150' 
  b. Run the main file to generate predictions 
> for example `python predict_multi.py -evaluate <path of evaluation set> -model <path of the model> -vocabulary <path to the vocabulary>
  c. The output can be found in the evaluation set with '_pred' surfix