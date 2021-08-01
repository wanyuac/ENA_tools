#!/usr/bin/env python

"""
Create an XML file from a tab-delimited (TSV) file about sequencing experiments for submission to the ENA database.
Except the header, each row of the TSV file defines an experiment using columns EXPERIMENT, STUDY_REF, TITLE, SAMPLE_DESCRIPTOR,
LIBRARY_STRATEGY, LIBRARY_SOURCE, LIBRARY_SELECTION, NOMINAL_LENGTH, NOMINAL_SDEV, library preparation date, INSTRUMENT_MODEL,
LIBRARY_CONSTRUCTION_PROTOCOL. (See ftp://ftp.ebi.ac.uk/pub/databases/ena/doc/xsd/sra_1_5/SRA.experiment.xsd)

Command line:
    python experimentTSV2XML.py experiments.tsv > experiments.xml

ENA's guidance on the XML structure:
    https://ena-docs.readthedocs.io/en/latest/submit/reads/programmatic.html

Copyright 2020 Yu Wan <wanyuac@126.com>
All rights reserved
Publication: 19 June 2020; last modification: 29 June 2020
"""

import os
import sys
import pandas as pd


def main():
    # Import the TSV file defining experiments
    if len(sys.argv) > 1:
        f_in = sys.argv[1]
        if os.path.exists(f_in):
            tab = pd.read_csv(sys.argv[1], index_col = "EXPERIMENT", sep = "\t", dtype = str)
        else:
            sys.exit("Input error: File " + f_in + " does not exist.")
    else:
        print("Argument error: An input TSV file is required.", file = sys.stderr)
        sys.exit(1)

    # Print the header
    print("<EXPERIMENT_SET>")

    # Loop through experiments
    for expr, row in tab.iterrows():  # row name, and a Series object
        print_experiment_block(expr, row)

    # Finish the XML file
    print("</EXPERIMENT_SET>")

    return


def print_experiment_block(expr, row):
    """
    Print a block of XML lines for each experiment
    """
    # Define white spaces of each level of lines
    T1 = "    "  # One tab
    T2 = T1 + T1  # Two tabs
    T3 = T2 + T1
    T4 = T3 + T1
    T5 = T4 + T1

    # Print lines
    print(T1 + "<EXPERIMENT alias=\"%s\">" % expr)
    print(T2 + "<TITLE>%s</TITLE>" % row["TITLE"])
    print(T2 + "<STUDY_REF accession=\"%s\"/>" % row["STUDY_REF"])

    ## Design
    print(T2 + "<DESIGN>")
    print(T3 + "<DESIGN_DESCRIPTION/>")  # A description can be added here.
    print(T3 + "<SAMPLE_DESCRIPTOR accession=\"%s\"/>" % row["SAMPLE_DESCRIPTOR"])  # The ERS number
    print(T3 + "<LIBRARY_DESCRIPTOR>")
    print(T4 + "<LIBRARY_NAME/>")  # Can have a value here
    print(T4 + "<LIBRARY_STRATEGY>%s</LIBRARY_STRATEGY>" % row["LIBRARY_STRATEGY"])
    print(T4 + "<LIBRARY_SOURCE>%s</LIBRARY_SOURCE>" % row["LIBRARY_SOURCE"])
    print(T4 + "<LIBRARY_SELECTION>%s</LIBRARY_SELECTION>" % row["LIBRARY_SELECTION"])
    print(T4 + "<LIBRARY_LAYOUT>")
    print(T5 + "<PAIRED NOMINAL_LENGTH=\"%s\" NOMINAL_SDEV=\"%s\"/>" % (row["NOMINAL_LENGTH"], row["NOMINAL_SDEV"]))
    print(T4 + "</LIBRARY_LAYOUT>")
    print(T4 + "<LIBRARY_CONSTRUCTION_PROTOCOL>%s</LIBRARY_CONSTRUCTION_PROTOCOL>" % row["LIBRARY_CONSTRUCTION_PROTOCOL"])
    print(T3 + "</LIBRARY_DESCRIPTOR>")
    print(T2 + "</DESIGN>")

    ## Platform
    print(T2 + "<PLATFORM>")
    print(T3 + "<ILLUMINA>")
    print(T4 + "<INSTRUMENT_MODEL>%s</INSTRUMENT_MODEL>" % row["INSTRUMENT_MODEL"])
    print(T3 + "</ILLUMINA>")
    print(T2 + "</PLATFORM>")

    ## Experiment attributes
    print(T2 + "<EXPERIMENT_ATTRIBUTES>")
    print(T3 + "<EXPERIMENT_ATTRIBUTE>")
    print(T4 + "<TAG>library preparation date</TAG>")
    print(T4 + "<VALUE>%s</VALUE>" % row["library preparation date"])
    print(T3 + "</EXPERIMENT_ATTRIBUTE>")
    print(T2 + "</EXPERIMENT_ATTRIBUTES>")

    ## Finish this experiment block
    print(T1 + "</EXPERIMENT>")

    return


if __name__ == "__main__":
    main()
