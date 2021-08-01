#!/usr/bin/env python

"""
Create a valid FASTA file from an input FASTA file for ENA assembly submission. This script performs two tasks:
    - Shortening contig names
    - Exclusion of contigs shorter than a predefined minimum length

Example command lines:
    python makeValidFASTA.py -i genome.fasta -m 200 -c contig -o genome_ena.fna

ENA's definition of valid files:
    https://ena-docs.readthedocs.io/en/latest/submit/assembly/genome.html?highlight=fasta#validation-rules

Copyright 2020 Yu Wan <wanyuac@126.com>
All rights reserved
Publication: 21 June 2020; last modification: 21 June 2020
"""

import sys
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from argparse import ArgumentParser

def parse_argument():
    parser = ArgumentParser(description = "Convert a TSV file to an XML file for registering samples to the ENA database")
    parser.add_argument("-i", dest = "i", type = str, required = True, help = "Path to the input FASTA file")
    parser.add_argument("-o", dest = "o", type = str, required = True, help = "Path to the output FASTA file")
    parser.add_argument("-m", dest = "m", type = int, required = False, default = 20, help = "Minimum contig length. Shorter contigs will be excluded from the output")
    parser.add_argument("-c", dest = "c", type = str, required = False, default = "contig", help = "Prefix of contig names")

    return parser.parse_args()


def main():
    args = parse_argument()   
    if args.c != "":
        prefix = args.c + "_"  # For example, contig_
    else:
        prefix = ""

    fasta_out = open(args.o, "w")
    n = 1
    for contig in SeqIO.parse(args.i, "fasta"):
        if len(contig.seq) >= args.m:
            contig.id = prefix + str(n)  # E.g., "contig_1" or "1"
            contig.name = ""
            contig.description = ""
            SeqIO.write(contig, fasta_out, "fasta")
            n += 1
        else:
            print("Warning: Skipped contig %s in file %s as it is shorter than %i." % (contig.id, args.o, args.m),\
                file = sys.stderr)
    fasta_out.close()

    return


if __name__ == "__main__":
    main()
