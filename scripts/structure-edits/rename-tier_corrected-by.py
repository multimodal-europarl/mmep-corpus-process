#!/usr/bin/env python3
"""
Chamge \<TIER TIER_ID="*_corrected_by">

to: \<TIER TIER_ID="*_manually_corrected">
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




def rename_corrected_tier(eaf):
    tiers = get_tiers(eaf)
    for tier in tiers:
        tier_id = tier.attrib.get("TIER_ID")
        if tier_id.endswith("_corrected_by"):
            iso = tier_id.split('_')[0]
            tier.attrib["TIER_ID"] = f"{iso}_manually_corrected"
    return eaf




def main(args):
    eaf_paths = sorted(list(eaf_iterator(tx_dir="mmep-corpus/transcribed-audio", start=args.start, end=args.end)))

    for ep in tqdm(eaf_paths, total=len(eaf_paths)):
        eaf = parse_eaf(ep)
        write_eaf(rename_corrected_tier(eaf), ep)




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument("-s", "--start", type=int, default=200809, help="Start: YYYYMM")
    parser.add_argument("-e", "--end", type=int, default=200912, help="End: YYYYMM")
    args = parser.parse_args()
    main(args)

