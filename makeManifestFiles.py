#!/usr/bin/env python

"""
Create manifest files from an input TSV file for multiple FASTA files for ENA assembly submission.

Example command lines:
    python makeManifestFiles.py .tsv -i manifest_all.tsv
    python makeManifestFiles.py .tsv -i manifest_all.tsv -o manifest -n STRAIN

ENA's description of manifest files:
    https://ena-docs.readthedocs.io/en/latest/submit/assembly/genome.html?highlight=fasta#

Copyright 2020 Yu Wan <wanyuac@126.com>
All rights reserved
Publication: 21 June 2020; last modification: 21 June 2020
"""

import os
import sys
import pandas as pd
from argparse import ArgumentParser


def parse_argument():
    parser = ArgumentParser(description = "Convert a TSV file to an XML file for registering samples to the ENA database")
    parser.add_argument("-i", dest = "i", type = str, required = True, help = "Path to the input TSV file defining information in manifest files")
    parser.add_argument("-o", dest = "o", type = str, required = False, default = ".", help = "Directory of output manifest files")
    parser.add_argument("-n", dest = "n", type = str, required = False, default = "ISOLATE", help = "Name of the column in the input file for row names and output filenames")

    return parser.parse_args()


def main():
    args = parse_argument()

    # Check output directory
    if args.o != ".":
        if not os.path.exists(args.o):
            os.mkdir(args.o)

    # Read the input TSV
    if os.path.exists(args.i):
        tab = pd.read_csv(args.i, index_col = args.n, sep = "\t", dtype = str)  # Returns a DataFrame object
    else:
        sys.exit("Input error: TSV file %s is not found." % args.i)

    # Iteratively create manifest files
    for sample, row in tab.iterrows():
        out_mani = open(os.path.join(args.o, sample + ".tsv"), "w")
        for key, val in row.iteritems():
            print("\t".join([key, val]), file = out_mani)
        out_mani.close()

    return


if __name__ == "__main__":
    main()
