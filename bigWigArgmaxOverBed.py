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

_default_score = 1000

def argmax_max(bed_data):
    if np.isnan(bed_data).all():
        bed_argmax = 0
        bed_max = np.nan
    else:
        bed_argmax = np.nanargmax(bed_data)
        bed_max = np.nanmax(bed_data)
    return bed_argmax, bed_max

def parse_bed_to_bed(bed_data):
    has_name = bed_data.shape[1]>=4
    has_strand= bed_data.shape[1]>=6
    for bed_line in bed_data.itertuples(index=True):
        i, chrom, start, end = bed_line[:4]
        bed_data = get_array(chrom, start, end)
        bed_argmax, bed_max = argmax_max(bed_data)
        bed_argmax = start+bed_argmax

        line = '%s\t%i\t%i' %(chrom, bed_argmax, bed_argmax+1)
        if has_name:
            line += '\t%s' % bed_line[4]
        else:
            line += '\t%i'%i

        if height and has_strand:
             line += '\t%.0f\t%s' % (bed_max, bed_line[6])
        elif has_strand and not height:
             line += '\t%i\t%s' % (_default_score, bed_line[6])
        elif height:
            line += '\t%.0f' % bed_max
        print(line)


def parse_bed_to_tsv(bed_data):
    has_name = bed_data.shape[1]>=4
    for bed_line in bed_data.itertuples(index=True):
        i, chrom, start, end = bed_line[:4]
        bed_data = get_array(chrom, start, end)
        bed_argmax, bed_max = argmax_max(bed_data)
        bed_argmax = start+bed_argmax
        if has_name:
            line = '%s\t%i' % (bed_line[4], bed_argmax)
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

data = pd.read_csv(in_bed, sep='\t', header=None).loc[:,:6]

if bed_out:
    parse_bed_to_bed(data)
else:
    parse_bed_to_tsv(data)
