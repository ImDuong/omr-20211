# import tensorflow as tf
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

print(tf.__version__)

from primus import CTC_PriMuS
import ctc_utils
import ctc_model
import argparse

import os

config = tf.ConfigProto()
config.gpu_options.allow_growth=True
tf.reset_default_graph()
sess = tf.InteractiveSession(config=config)

parser = argparse.ArgumentParser(description='Train model.')
parser.add_argument('-corpus', dest='corpus', type=str, required=True, help='Path to the corpus.')
parser.add_argument('-set',  dest='set', type=str, required=True, help='Path to the set file.')
parser.add_argument('-model', dest='model', type=str, required=False, default=None, help='Path to the trained model.')
parser.add_argument('-save_model', dest='save_model', type=str, required=True, help='Path to save the model.')
parser.add_argument('-vocabulary', dest='voc', type=str, required=True, help='Path to the vocabulary file.')
parser.add_argument('-semantic', dest='semantic', action="store_true", default=False)
args = parser.parse_args()

# Load primus

primus = CTC_PriMuS(args.corpus,args.set,args.voc, args.semantic, val_split = 0.05)

# Parameterization
img_height = 128
max_epochs = 64000
dropout = 0.5

# Model
params = ctc_model.default_model_params(img_height,primus.vocabulary_size)

if args.model is not None: 
    saver = tf.train.import_meta_graph(args.model)
    saver.restore(sess,args.model[:-5])
    # saver.restore(sess,tf.train.latest_checkpoint('/content/trained_model/'))

    graph = tf.get_default_graph()

    inputs = graph.get_tensor_by_name("model_input:0")
    seq_len = graph.get_tensor_by_name("seq_lengths:0")
    rnn_keep_prob = graph.get_tensor_by_name("keep_prob:0")
    height_tensor = graph.get_tensor_by_name("input_height:0")
    width_reduction_tensor = graph.get_tensor_by_name("width_reduction:0")
    logits = tf.get_collection("logits")[0]

    decoded, _ = tf.nn.ctc_greedy_decoder(logits, seq_len)

    # targets = graph.get_tensor_by_name("target:0")
    targets = tf.sparse_placeholder(dtype=tf.int32, name='target')
    ctc_loss = tf.nn.ctc_loss(labels=targets, inputs=logits, sequence_length=seq_len, time_major=True)
    loss = tf.reduce_mean(ctc_loss)

    train_opt = tf.train.AdamOptimizer(name='MyNewAdam').minimize(loss)

    uninitialized_vars = []
    # for var in tf.global_variables():
    for var in tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES):
        try:
            sess.run(var)
        except tf.errors.FailedPreconditionError:
            uninitialized_vars.append(var)

    sess.run(tf.variables_initializer(uninitialized_vars))

    epoch = int(args.model.split('-')[-1].replace('.meta', ''))
else:
    inputs, seq_len, targets, decoded, loss, rnn_keep_prob = ctc_model.ctc_crnn(params)

    saver = tf.train.Saver(max_to_keep=None)
    sess.run(tf.global_variables_initializer())

    epoch = 0

    train_opt = tf.train.AdamOptimizer().minimize(loss)

print("epoch: ", epoch)

# Training loop
for epoch in range(epoch + 1, max_epochs):
    batch = primus.nextBatch(params)

    _, loss_value = sess.run([train_opt, loss],
                             feed_dict={
                                inputs: batch['inputs'],
                                seq_len: batch['seq_lengths'],
                                targets: ctc_utils.sparse_tuple_from(batch['targets']),
                                rnn_keep_prob: dropout,
                            })

    print(f"Epoch {epoch}'s loss value: {loss_value}")
    if epoch % 500 == 0:
        # VALIDATION
        print ('Loss value at epoch ' + str(epoch) + ':' + str(loss_value))
        print ('Validating...')

        validation_batch, validation_size = primus.getValidation(params)
        
        val_idx = 0
        
        val_ed = 0
        val_len = 0
        val_count = 0
            
        while val_idx < validation_size:
            print(val_idx)

            mini_batch_feed_dict = {
                inputs: validation_batch['inputs'][val_idx:val_idx+params['batch_size']],
                seq_len: validation_batch['seq_lengths'][val_idx:val_idx+params['batch_size']],
                rnn_keep_prob: 1.0            
            }            
                        
            prediction = sess.run(decoded,
                                  mini_batch_feed_dict)

            str_predictions = ctc_utils.sparse_tensor_to_strs(prediction)

            print(str_predictions)

            for i in range(len(str_predictions)):
                ed = ctc_utils.edit_distance(str_predictions[i], validation_batch['targets'][val_idx+i])
                val_ed = val_ed + ed
                val_len = val_len + len(validation_batch['targets'][val_idx+i])
                val_count = val_count + 1
                
            val_idx = val_idx + params['batch_size']

    
        print ('[Epoch ' + str(epoch) + '] ' + str(1. * val_ed / val_count) + ' (' + str(100. * val_ed / val_len) + ' SER) from ' + str(val_count) + ' samples.')        
        print ('Saving the model...')
        saver.save(sess,args.save_model,global_step=epoch)
        print ('------------------------------')
