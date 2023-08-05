#!/usr/bin/env python
import argparse
from sarscov2formatter import formatter


def main():
	parser = argparse.ArgumentParser(description='Metadata extractor for SARS-CoV-2 selection analysis pipeline in Galaxy')
	parser.add_argument('-a', '--alignment', dest='alignment', action='store', help='Mulitple sequence alignment file', required=True)
	parser.add_argument('-m', '--metadata', dest='metadata', action='store', help='Metadata source (Use "ncbi" if using NCBI SARS-CoV-2 data, otherwise supply tabular file of the correct format)', required=True)
	args = parser.parse_args()

	formatter(args.alignment, args.metadata)

if __name__ == '__main__':
    exit(main())