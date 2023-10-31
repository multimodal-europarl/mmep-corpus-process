#!/usr/bin/env python3
"""
Chamge <TIER LINFUISTIC_TYPE_REF="corrected_by">

to: <TIER LINFUISTIC_TYPE_REF="Transcription_Dependent">
"""
from pymmep.eaf_utils import (
        eaf_iterator,
        get_tiers,
        parse_eaf,
        write_eaf,
    )
from tqdm import tqdm
from lxml import etree
import argparse




def rename_type_ref(eaf):
    tiers = get_tiers(eaf)
    for tier in tiers:
        if tier.attrib.get("LINGUISTIC_TYPE_REF") == "corrected_by":
            tier.attrib["LINGUISTIC_TYPE_REF"] = "Transcription_Dependent"
    return eaf




def main(args):
    eaf_paths = sorted(list(eaf_iterator(tx_dir="mmep-corpus/transcribed-audio", start=args.start, end=args.end)))

    for ep in tqdm(eaf_paths, total=len(eaf_paths)):
        eaf = parse_eaf(ep)
        write_eaf(rename_type_ref(eaf), ep)




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument("-s", "--start", type=int, default=200809, help="Start: YYYYMM")
    parser.add_argument("-e", "--end", type=int, default=200912, help="End: YYYYMM")
    args = parser.parse_args()
    main(args)

