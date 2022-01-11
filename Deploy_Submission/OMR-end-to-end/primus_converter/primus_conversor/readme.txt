Examples of use of semantic_conversor.sh.

000100196-1_2_2.* are the original PRIMUS files.

1. Using an input file.
semantic_conversor.sh 000100973-1_1_2.semantic output.mid
or
semantic_conversor.sh 000100973-1_1_2.semantic output.mei

2. Using standard input
echo <semantic string> | semantic_conversor.sh output.mid
or with output.mei

NOTE: MIDI input contains the right pitches and durations, but key signatures may not be consistent yet