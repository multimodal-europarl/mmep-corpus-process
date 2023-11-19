#!/usr/bin/env python3
"""
Replace duplicated time stamp IDs with unique ones.
"""
from lxml import etree
from pymmep.eaf_utils import (
    eaf_iterator,
    get_tiers,
    get_time_slots,
    make_time_slot_dictionary,
    parse_eaf,
    write_eaf,
)
from tqdm import tqdm
import argparse




def replace_timeslot_ids(eaf):
    time_order = eaf.find('TIME_ORDER')
    ts_dict = make_time_slot_dictionary(get_time_slots(eaf))
    [e.getparent().remove(e) for e in time_order]
    running_ts = 1
    tiers = get_tiers(eaf, tx_only=True)
    for tier in tiers:
        for annotation in tier:
            old_ts_1 = annotation[0].attrib.get("TIME_SLOT_REF1")
            old_ts_2 = annotation[0].attrib.get("TIME_SLOT_REF2")

            annotation[0].attrib["TIME_SLOT_REF1"] = f"ts{running_ts}"
            ts = etree.SubElement(time_order, "TIME_SLOT")
            ts.attrib["TIME_SLOT_ID"] = f"ts{running_ts}"
            ts.attrib["TIME_VALUE"] = str(ts_dict[old_ts_1])
            #print(old_ts_1, f"ts{running_ts}", str(ts_dict[old_ts_1]))
            running_ts += 1

            annotation[0].attrib["TIME_SLOT_REF2"] = f"ts{running_ts}"
            ts = etree.SubElement(time_order, "TIME_SLOT")
            ts.attrib["TIME_SLOT_ID"] = f"ts{running_ts}"
            ts.attrib["TIME_VALUE"] = str(ts_dict[old_ts_2])
            #print(old_ts_2, f"ts{running_ts}", str(ts_dict[old_ts_2]))
            running_ts += 1
    return eaf




def main(args):
    eaf_paths = sorted(list(eaf_iterator(tx_dir="mmep-corpus/transcribed-audio", start=args.start, end=args.end)))

    for ep in tqdm(eaf_paths, total=len(eaf_paths)):
        write_eaf(replace_timeslot_ids(parse_eaf(ep)), ep)




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument("-s", "--start", type=int, default=200809, help="Start: YYYYMM")
    parser.add_argument("-e", "--end", type=int, default=201005, help="End: YYYYMM")
    args = parser.parse_args()
    main(args)
