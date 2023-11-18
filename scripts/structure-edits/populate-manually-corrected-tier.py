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




def populate_manual_tier(eaf, ep):
    tiers = get_tiers(eaf, tx_only=True)
    #print(len(tiers), tiers)
    if len(tiers) == 1:
        print("empty eaf:", ep)
        return eaf
    for tier in tiers:
        tier_id = tier.attrib.get("TIER_ID")
        try:
            iso = tier_id.split('_')[1]
        except:
            print("can't find iso code:", ep)
            return eaf
        correction_tier = eaf.find(f"TIER[@TIER_ID='{iso}_manually_corrected']")
        if len(correction_tier) == 0:
            correction_tier.text = None
        tx_ids = []
        for annotation in tier:
            tx_ids.append(annotation[0].attrib.get("ANNOTATION_ID"))
        for annotation in correction_tier:
            cta_ref = annotation[0].attrib.get("ANNOTATION_REF")
            if cta_ref in tx_ids:
                tx_ids.remove(cta_ref)
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
        #print(ep)
        eaf = parse_eaf(ep)
        write_eaf(populate_manual_tier(eaf, ep), ep)




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument("-s", "--start", type=int, default=200809, help="Start: YYYYMM")
    parser.add_argument("-e", "--end", type=int, default=201005, help="End: YYYYMM")
    args = parser.parse_args()
    main(args)

