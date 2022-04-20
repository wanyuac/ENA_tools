#!/usr/bin/env python

"""
Create an XML file from a tab-delimited (TSV) file for register samples programmatically to the ENA database

Example command lines:
    python sampleTSV2XML.py -i samples.tsv -s > samples.xml
    python sampleTSV2XML.py -i samples.tsv -a attrs.txt -c ERC000028 > samples.xml

ENA's guidance on the XML structure:
    https://ena-docs.readthedocs.io/en/latest/submit/samples/programmatic.html

The input TSV file for argument '-i':
    Mandatory column names in the TSV file for argument -i: TITLE, isolate or strain, host, host health state, collection date,
    geographic location (country and/or sea), TAXON_ID, SCIENTIFIC_NAME. Columns TITLE, TAXON_ID, and SCIENTIFIC_NAME are not
    considered as sample attributes. So they should not be included for the -a parameter. Moreover, "isolate" or "strain" should
    not be put in the list of sample attributes.

Argument '-a': This argument is designed for including a subset of attribute columns (from the input TSV file) into the output XML
    file so users have some flexibility in determining the content in the output file.

Copyright (C) 2020-2022 Yu Wan <wanyuac@126.com>
Licensed under the GNU General Public Licence version 3 (GPLv3) <https://www.gnu.org/licenses/>.
Publication: 18 June 2020; last modification: 19 April 2022
"""

import os
import sys
import pandas
from argparse import ArgumentParser


def parse_arguments():
    parser = ArgumentParser(description = "Convert a TSV file to an XML file for registering samples to the ENA database")
    parser.add_argument("-i", dest = "i", type = str, required = True, help = "Path to an input TSV file containing at least a column \'isolate\' or \'strain\' and possibly columns of attributes.")
    parser.add_argument("-s", dest = "s", action = "store_true", required = False, help = "(Optional) Set it to choose column \"strain\" for indices. Otherwise, column \"isolate\" will be used.")
    parser.add_argument("-a", dest = "a", type = str, required = False, default = None, help = "(Optional) Path to a text file listing names of sample attributes (excluding 'isolate' and 'strain') listed in the input TSV file (\'-i\'). One attribute name per line.")  # Path to a text file specifying columns for sample attributes.
    parser.add_argument("-c", dest = "c", type = str, required = False, default = None, help = "(Optional) Accession number of ENA's sample checklist, such as ERC000028")  # Path to a text file specifying columns for sample attributes.
    parser.add_argument("-t", dest = "t", type = str, required = False, default = "", help = "(Optional) Name of the centre in which the primary investigator has worked")
    return parser.parse_args()


def main():
    # Read the input TSV file
    args = parse_arguments()
    attrs = import_attribute_names(args.a)
    id_col = "strain" if args.s else "isolate"
    if os.path.exists(args.i):
        try:
            tab = pandas.read_csv(args.i, index_col = id_col, sep = "\t", dtype = str)  # Returns a DataFrame object
        except (KeyError, ValueError):
            sys.exit("Error: neither 'isolate' nor 'strain' is found in column names.")
    else:
        sys.exit("Input error: TSV file %s is not found." % args.i)
    
    # Print header lines
    print("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
    print("<SAMPLE_SET>")

    # Iterate through rows and print a SAMPLE block for each sample
    for sample, row in tab.iterrows():  # row name, and a Series object
        print_sample_block(sample, row, attrs, args.c, args.s, args.t)

    # Finish the XML file with the line below
    print("</SAMPLE_SET>")

    return


def print_sample_block(sample, row, attrs, checklist, use_strain, centre):
    """
    Print a block of XML code for each sample
    """
    # Set spaces for tab keys
    T1 = "    "  # Space for a single tab key
    T2 = T1 + T1
    T3 = T2 + T1
    T4 = T3 + T1

    # Print headers of the current block
    print(T1 + "<SAMPLE alias=\"%s\" center_name=\"%s\">" % (sample, centre))
    print(T2 + "<TITLE>%s</TITLE>" % row["TITLE"])

    # Print sample name and taxonomical information
    print(T2 + "<SAMPLE_NAME>")
    print(T3 + "<TAXON_ID>%s</TAXON_ID>" % row["TAXON_ID"])
    print(T3 + "<SCIENTIFIC_NAME>%s</SCIENTIFIC_NAME>" % row["SCIENTIFIC_NAME"])
    print(T3 + "<COMMON_NAME></COMMON_NAME>")
    print(T2 + "</SAMPLE_NAME>")

    # Print sample attributes
    print(T2 + "<SAMPLE_ATTRIBUTES>")
    
    ## Specify ENA's sample checklist when it is specified
    ## See ena-docs.readthedocs.io/en/latest/submit/samples/programmatic.html for details.
    if checklist != None:
        print(T3 + "<SAMPLE_ATTRIBUTE>")
        print(T4 + "<TAG>ENA-CHECKLIST</TAG>")
        print(T4 + "<VALUE>%s</VALUE>" % checklist)
        print(T3 + "</SAMPLE_ATTRIBUTE>")
    
    # Print isolate/strain name
    # "isolate/strain" is not put in the list attrs of attributes because row names cannot be retrived using syntax row[a].
    print(T3 + "<SAMPLE_ATTRIBUTE>")
    if use_strain:
        print(T4 + "<TAG>strain</TAG>")
    else:
        print(T4 + "<TAG>isolate</TAG>")
    print(T4 + "<VALUE>%s</VALUE>" % sample)
    print(T3 + "</SAMPLE_ATTRIBUTE>")
    
    """
	Print other attributes: attribute names are listed in the input text file for argument '-a' and attribute values are
	listed in corresponding columns in the input TSV file for argument '-i'.
	"""
    for a in attrs:
        print(T3 + "<SAMPLE_ATTRIBUTE>")
        print(T4 + "<TAG>%s</TAG>" % a)
        print(T4 + "<VALUE>%s</VALUE>" % row[a])
        print(T3 + "</SAMPLE_ATTRIBUTE>")
    print(T2 + "</SAMPLE_ATTRIBUTES>")

    # Finish the current sample block
    print(T1 + "</SAMPLE>")

    return


def import_attribute_names(a):
    """
    Read sample attribute names when f != None.
    """
    if a == None:  # Default value: ENA's mandatory fields of sample metadata
        attrs = ["host", "host health state", "collection date", "geographic location (country and/or sea)"]
    else:  # Read attribute names from a text file
        with open(a, "r") as f:
            attrs = f.read().splitlines()

    return attrs


if __name__ == "__main__":
    main()
