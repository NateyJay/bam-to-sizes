#!/usr/bin/env python3

from collections import Counter
from pprint import pprint
import sys
from subprocess import Popen, PIPE
import argparse



parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', 
	required=True,
	nargs="?",
	help='bamfile input')
parser.add_argument('-o', '--output_file', 
	required=False,
	default = False,
	type=str,
	help='names the prefix.size.txt')
parser.add_argument('-t', '--test_run',
	action='store_true',
	default=False,
	help='performs action recording only the first 100 spots')

args = parser.parse_args()
file = args.file
test_run = args.test_run
output_file = args.output_file

def samtools(file):

	samtools = Popen(["samtools", "view", "-@", "4", file], stdout=PIPE, stderr=PIPE, universal_newlines=True)
	
	for stdout_line in iter(samtools.stdout.readline, ""):
		yield stdout_line 
	samtools.stdout.close()
	return_code = samtools.wait()
	if return_code:
		return
		raise CalledProcessError(return_code, samtools.stderr.readlines())


rg_i = False
c = Counter()

rgs = set()
sizes = set()

for i, line in enumerate(samtools(file)):
	if test_run:
		if i == 1000000:
			break

	if i % 5000000 == 0:
		print(i)

	# print(line)

	line = line.strip().split("\t")

	if not rg_i:
		for i,j in enumerate(line):
			if "RG:Z:" in j:
				rg_i = i
				break

	size = len(line[9])
	flag = int(line[1])
	rg   = line[rg_i][5:]

	rgs.add(rg)
	sizes.add(size)

	key= f"{size}_{rg}"
	c.update([key])


sizes = sorted(list(sizes))
rgs = sorted(list(rgs))

if output_file:
	outf = open(output_file, 'w')
else:
	outf = sys.stdout

print("size", "\t".join(rgs), sep='\t', file=outf)

for size in range(min(sizes), max(sizes)+1):

	abds = [c[f"{size}_{rg}"] for rg in rgs]

	print(size, "\t".join(map(str, abds)), sep='\t', file=outf)

if output_file:
	outf.close()





