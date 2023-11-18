#!/usr/bin/env python3
"""
Change non-unique elan-generated ids to formatted uuids. Run any time Annotations are added or split in Elan.
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




def update_annotation_ids(eaf):
    """
    Check all annotation IDs. If assigned by elan, replace.
    """
    tiers = get_tiers(eaf)
    D = {}
    UUIDS = set()
    num_ids = 0
    for tier in tiers:
        #print(tier, tier.tag, tier.attrib.get("TIER_ID"), xml_formatted_uuid())
        for annotation in tier:
            ID = annotation[0].attrib.get("ANNOTATION_ID")
        #    print(ID)
            if ID.startswith("a"):
                new_id = xml_formatted_uuid()
                D[ID] = new_id
                annotation[0].attrib["ANNOTATION_ID"] = new_id
                num_ids += 1
                UUIDS.add(new_id)
    assert len(UUIDS) == num_ids
    for tier in tiers:
        if tier.attrib.get("LINGUISTIC_TYPE_REF") != "default-lt":
            for annotation in tier:
                ref = annotation[0].attrib.get("ANNOTATION_REF")
                if ref.startswith("a"):
                    annotation[0].attrib["ANNOTATION_REF"] = D[ref]
    return eaf





def main(args):
    """
Iterate over all eaf files, parse, and update_annotation_ids()
```
usage:
update-annotation-ids.py [-h] [-s START] [-e END]

Change non-unique elan-generated ids to formatted uuids.
Run any time Annotations are added or split in Elan.

options:
  -h, --help            show this help message and exit
  -s START, --start START
                        Start: YYYYMM
  -e END, --end END     End: YYYYMM
    ```
    """
    eaf_paths = sorted(list(eaf_iterator(tx_dir="mmep-corpus/transcribed-audio", start=args.start, end=args.end)))

    for ep in tqdm(eaf_paths, total=len(eaf_paths)):
        eaf = parse_eaf(ep)
        write_eaf(update_annotation_ids(eaf), ep)




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument("-s", "--start", type=int, default=200809, help="Start: YYYYMM")
    parser.add_argument("-e", "--end", type=int, default=201005, help="End: YYYYMM")
    args = parser.parse_args()
    main(args)
