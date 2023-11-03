#!/usr/bin/env python3
"""
Popoulate \<TIER TIER_ID="*_manually_corrected"> with REF_ANNOTATIONS.
"""
from pymmep.eaf_utils import (
        eaf_iterator,
        get_tiers,
        parse_eaf,
        write_eaf,
        xml_formatted_uuid,
    )
from tqdm import tqdm
from lxml import etree
import argparse




def populate_manual_tier(eaf):
    tiers = get_tiers(eaf, tx_only=True)
    for tier in tiers:
        tier_id = tier.attrib.get("TIER_ID")
        iso = tier_id.split('_')[1]
        correction_tier = eaf.find(f"TIER[@TIER_ID='{iso}_manually_corrected']")
        tx_ids = []
        for annotation in tier:
            tx_ids.append(annotation[0].attrib.get("ANNOTATION_ID"))
        for tx_id in tx_ids:
            A = etree.SubElement(correction_tier, "ANNOTATION")
            R = etree.SubElement(A, "REF_ANNOTATION")
            R.attrib["ANNOTATION_REF"] = tx_id
            R.attrib["ANNOTATION_ID"] = xml_formatted_uuid()
            V = etree.SubElement(R, "ANNOTATION_VALUE")
            V.text = "False"
    return eaf




def main(args):
    eaf_paths = sorted(list(eaf_iterator(tx_dir="mmep-corpus/transcribed-audio", start=args.start, end=args.end)))

    for ep in tqdm(eaf_paths, total=len(eaf_paths)):
        eaf = parse_eaf(ep)
        write_eaf(populate_manual_tier(eaf), ep)




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument("-s", "--start", type=int, default=200809, help="Start: YYYYMM")
    parser.add_argument("-e", "--end", type=int, default=200912, help="End: YYYYMM")
    args = parser.parse_args()
    main(args)

