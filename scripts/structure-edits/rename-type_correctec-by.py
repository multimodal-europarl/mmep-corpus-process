#!/usr/bin/env python3
"""
Chamge <LINGUISTIC_TYPE LINFUISTIC_TYPE_ID="corrected_by">

to: <LINGUISTIC_TYPE LINFUISTIC_TYPE_ID="Transcription_Dependent">
"""
from pymmep.eaf_utils import (
        eaf_iterator,
        parse_eaf,
        write_eaf,
    )
from tqdm import tqdm
from lxml import etree
import argparse




def rename_ling_type(eaf):
    lingtyps = eaf.findall("LINGUISTIC_TYPE")
    for lt in lingtyps:
        if lt.attrib.get("LINGUISTIC_TYPE_ID") == "corrected_by":
            lt.attrib["LINGUISTIC_TYPE_ID"] = "Transcription_Dependent"
    return eaf




def main(args):
    eaf_paths = sorted(list(eaf_iterator(tx_dir="mmep-corpus/transcribed-audio", start=args.start, end=args.end)))

    for ep in tqdm(eaf_paths, total=len(eaf_paths)):
        eaf = parse_eaf(ep)
        write_eaf(rename_ling_type(eaf), ep)




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument("-s", "--start", type=int, default=200809, help="Start: YYYYMM")
    parser.add_argument("-e", "--end", type=int, default=200912, help="End: YYYYMM")
    args = parser.parse_args()
    main(args)

