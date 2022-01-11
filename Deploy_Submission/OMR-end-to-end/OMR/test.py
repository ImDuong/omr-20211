# python OMR/ctc_predict.py -image Datastore/imgs/000051652-1_2_1.png -model
# Models/semantic_model.meta -vocabulary Data/vocabulary_semantic.txt -output Datastore/semantics/output.txt


from midi2audio import FluidSynth
FluidSynth().play_midi('62a06c6471624e4891e92003006237b1.mid')


# FluidSynth().midi_to_audio('../Datastore/midi/62a06c6471624e4891e92003006237b1.mid', 'output.wav')