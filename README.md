# bam-to-sizes
 A simple python script to quantify abundances of aligned sRNA reads by size and readgroup.

This is meant to be used on a merged_alignments.bam file produce from an alignment using ShortStack. It searches for the size and readgroup of aligned reads and counts them.

usage:
```
bam-to-sizes.py -f merged_alignments.bam -o output_file.txt

## run with -t to test the output of your run
## without an output -o specified it will print to stdout
```


