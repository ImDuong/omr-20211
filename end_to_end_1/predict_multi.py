import os
import argparse
import tensorflow as tf
import ctc_utils
import cv2
import numpy as np
import glob

parser = argparse.ArgumentParser(description='Decode a music score image with a trained model (CTC).')
parser.add_argument('-evaluate',  dest='eval', type=str, required=True, help='Path to the evaluation set.')
parser.add_argument('-model', dest='model', type=str, required=True, help='Path to the trained model.')
parser.add_argument('-vocabulary', dest='voc_file', type=str, required=True, help='Path to the vocabulary file.')
args = parser.parse_args()

tf.reset_default_graph()
sess = tf.InteractiveSession()

# Read the dictionary
dict_file = open(args.voc_file,'r')
dict_list = dict_file.read().splitlines()
int2word = dict()
for word in dict_list:
    word_idx = len(int2word)
    int2word[word_idx] = word
dict_file.close()

# Restore weights
saver = tf.train.import_meta_graph(args.model)
saver.restore(sess,args.model[:-5])

graph = tf.get_default_graph()

input = graph.get_tensor_by_name("model_input:0")
seq_len = graph.get_tensor_by_name("seq_lengths:0")
rnn_keep_prob = graph.get_tensor_by_name("keep_prob:0")
height_tensor = graph.get_tensor_by_name("input_height:0")
width_reduction_tensor = graph.get_tensor_by_name("width_reduction:0")
logits = tf.get_collection("logits")[0]

# Constants that are saved inside the model itself
WIDTH_REDUCTION, HEIGHT = sess.run([width_reduction_tensor, height_tensor])

decoded, _ = tf.nn.ctc_greedy_decoder(logits, seq_len)

list_of_images = []
for image in glob.glob(f'{args.eval}/*/*.png'):
    image_n = os.path.basename(image)
    list_of_images.append(image_n)

for img in list_of_images:
    filename = img.split('.')[0]
    folderpath = os.path.join(args.eval, filename)
    filepath = os.path.join(folderpath, img)

    image = cv2.imread(filepath,False)
    image = ctc_utils.resize(image, HEIGHT)
    image = ctc_utils.normalize(image)
    image = np.asarray(image).reshape(1,image.shape[0],image.shape[1],1)

    seq_lengths = [ image.shape[2] / WIDTH_REDUCTION ]

    prediction = sess.run(decoded,
                        feed_dict={
                            input: image,
                            seq_len: seq_lengths,
                            rnn_keep_prob: 1.0,
                        })

    str_predictions = ctc_utils.sparse_tensor_to_strs(prediction)

    to_write = []
    for w in str_predictions[0]:
        to_write.append(int2word[w])
        print (int2word[w], end='\t')

    print('\n')
    outpath = f'{os.path.join(folderpath, filename)}_pred.semantic'

    with open(outpath, 'w+') as f:
        f.write('\t'.join(to_write))

