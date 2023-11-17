#!/usr/bin/env python3
"""
Just pretty print the eaf documents.

The eaf docs were generated with a different xml library, so in order to avoid getting git diffs for new line characters and the like, this script will just read and write docs over again with the same pretty print function, so we don't end up with this junk in diffs of "real" edits.
"""
from pymmep.eaf_utils import (
        eaf_iterator,
        parse_eaf,
        write_eaf,
    )
from tqdm import tqdm
from lxml import etree
import argparse

def main(args):
    eaf_paths = sorted(list(eaf_iterator(tx_dir="mmep-corpus/transcribed-audio", start=args.start, end=args.end)))

    for ep in tqdm(eaf_paths, total=len(eaf_paths)):
        eaf = parse_eaf(ep)
        write_eaf(eaf, ep)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument("-s", "--start", type=int, default=200809, help="Start: YYYYMM")
    parser.add_argument("-e", "--end", type=int, default=201005, help="End: YYYYMM")
    args = parser.parse_args()
    main(args)

