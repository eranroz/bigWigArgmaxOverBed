#!/usr/bin/env python

"""
bigWigArgmaxOverBed - Compute the argmax position of bigWig over each bed.

usage: %prog in.bw in.bed
   -h, --height: include the height in additional column
   -z, --zero: treat non covered as zero
   --bedOut: output as bed file

The output columns are:
   name - For bed with name field (otherwise skipped)
   argmax - position of argmax within each bed
"""
import numpy as np
import pandas as pd
from bx.bbi.bigwig_file import BigWigFile
from bx.cookbook import doc_optparse

def argmax_max(bed_data):
    if np.isnan(bed_data).all():
        bed_argmax = 0
        bed_max = np.nan
    else:
        bed_argmax = np.nanargmax(bed_data)
        bed_max = np.nanmax(bed_data)
    return bed_argmax, bed_max


def parse_bed_with_names(bed_csv):
    for chrom, start, end, name in bed_csv.itertuples(index=False):
        bed_data = get_array(chrom, start, end)
        bed_argmax, bed_max = argmax_max(bed_data)
        bed_argmax = start+bed_argmax
        if bed_out:
            line = '%s\t%i\t%i\t%s'%(chrom,bed_argmax, bed_argmax, name)
        else:
            line = '%s\t%i'%(name, bed_argmax)
        if height:
            line+='\t%.0f' % bed_max
        print(line)

def parse_bed(bed_data):
    for chrom, start, end in bed_data.itertuples(index=False):
        bed_data = get_array(chrom, start, end)
        bed_argmax, bed_max = argmax_max(bed_data)
        bed_argmax = start+bed_argmax

        if bed_out:
            line = '%s\t%i\t%i' %(chrom, bed_argmax, bed_argmax)
        else:
            line = '%i' % bed_argmax
        if height:
            line += '\t%.0f' % bed_max
        print(line)

options, args = doc_optparse.parse(__doc__)
try:
    height = options.height
    zero = options.zero or options.bedOut  # bedOut implicitly means zero
    bed_out = options.bedOut

    in_bigwig, in_bed = args
except:
    doc_optparse.exit()

bw_input = BigWigFile(open(in_bigwig, 'rb'))
if zero:
    get_array = lambda chrom, start, end: np.nan_to_num(bw_input.get_as_array(chrom, start, end))
else:
    get_array = lambda chrom, start, end: bw_input.get_as_array(chrom, start, end)

try:
    data = pd.read_csv(in_bed, names=['chrom', 'start', 'end', 'name'], sep='\s+', header=None, usecols=[0, 1, 2, 3])
    named = True
except ValueError:
    data = pd.read_csv(in_bed, names=['chrom', 'start', 'end'], sep='\s+', header=None, usecols=[0, 1, 2])
    named = False

if named:
    parse_bed_with_names(data)
else:
    parse_bed(data)
