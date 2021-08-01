#!/usr/bin/env python

"""
Create an XML file from a tab-delimited (TSV) file about sequencing runs for submission to the ENA database.
Except the header, each row of the TSV file defines a sequencing run under a registered experiment using columns
RUN, EXPERIMENT, R1, R1_MD5, R2, R2_MD5.

Command line:
    python runTSV2XML.py runs.tsv > runs.xml

ENA's guidance on the XML structure:
    https://ena-docs.readthedocs.io/en/latest/submit/reads/programmatic.html

Copyright 2020 Yu Wan <wanyuac@126.com>
All rights reserved
Publication: 20 June 2020 (summer solstice); last modification: 20 June 2020
"""

import sys
import pandas as pd


def main():
    # Import the TSV file defining runs
    if len(sys.argv) > 1:
        tab = pd.read_csv(sys.argv[1], index_col = "RUN", sep = "\t", dtype = str)
    else:
        print("Argument error: An input TSV file is required.", file = sys.stderr)
        sys.exit(1)

    # Print the header
    print("<RUN_SET>")

    # Loop through run records
    for run, row in tab.iterrows():  # row name, and a Series object
        print_run_block(run, row)

    # Finish the XML file
    print("</RUN_SET>")

    return


def print_run_block(run, row):
    """
    Print a block of XML lines for each sequencing run
    """
    # Define white spaces of each level of lines
    T1 = "    "  # One tab
    T2 = T1 + T1  # Two tabs
    T3 = T2 + T1
    T4 = T3 + T1

    # Print the block
    print(T1 + "<RUN alias=\"%s\" center_name=\"\">" % run)
    print(T2 + "<EXPERIMENT_REF refname=\"%s\"/>" % row["EXPERIMENT"])  # This specification links the current run to an experiment
    print(T2 + "<DATA_BLOCK>")
    print(T3 + "<FILES>")
    print(T4 + "<FILE filename=\"%s\" filetype=\"fastq\" checksum_method=\"MD5\" checksum=\"%s\"/>" % (row["R1"], row["R1_MD5"]))
    print(T4 + "<FILE filename=\"%s\" filetype=\"fastq\" checksum_method=\"MD5\" checksum=\"%s\"/>" % (row["R2"], row["R2_MD5"]))
    print(T3 + "</FILES>")
    print(T2 + "</DATA_BLOCK>")
    print(T1 + "</RUN>")

    return


if __name__ == "__main__":
    main()
