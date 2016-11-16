#!/usr/bin/env python

"""
bigWigArgmaxOverBed - Compute the argmax score of big wig over each bed.

usage: %prog in.bw in.bed
   -h, --height: include the height in additional column
   -z, --zero: treat non covered as zero


The output columns are:
   name - name field from bed, which should be unique (if bed has name column)
   argmax - position of argmax within each bed
"""
import numpy as np
import pandas as pd
from pandas.io.common import CParserError
from bx.bbi.bigwig_file import BigWigFile
from bx.cookbook import doc_optparse


def parse_bed_with_names(bed_csv):
    for chrom, start, end, name in bed_csv.itertuples(index=False):
        bed_data = get_array(chrom, start, end)
        if height:
            print('%s\t%f\t%f' % (name, start + bed_data.argmax(), bed_data.max()))
        else:
            print('%s\t%s' % (name, start + bed_data.argmax()))


def parse_bed(bed_data):
    for chrom, start, end in bed_data.itertuples(index=False):
        bed_data = get_array(chrom, start, end)
        if height:
            print('%f\t%f' % (start + bed_data.argmax(), bed_data.max()))
        else:
            print('%f' % (start + bed_data.argmax()))


options, args = doc_optparse.parse(__doc__)
try:
    height = options.height
    zero = options.zero
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
except CParserError:
    data = pd.read_csv(in_bed, names=['chrom', 'start', 'end'], sep='\s+', header=None, usecols=[0, 1, 2])
    named = False

if named:
    parse_bed_with_names(data)
else:
    parse_bed(data)
