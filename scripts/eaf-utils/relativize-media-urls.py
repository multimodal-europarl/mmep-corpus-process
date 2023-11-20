#!/usr/bin/env python3
"""
Reset MEDIA_URL and RELATIVE_MEDIA_URL to a relative media url.

This should be done after every time working with files in Elan
    - to avoid creating diffs due to changing absolute media paths
    - to avoid creating diffs due to non-lxml-style pretty print
"""
from lxml import etree
from pymmep.eaf_utils import (
        eaf_iterator,
        get_media_descriptors,
        parse_eaf,
        write_eaf,
    )
from tqdm import tqdm
import argparse, os




def reset_media_descriptors(ep):
    """
    Set both media descriptors to relative path.
    """
    a, b, month, dirname, filename = ep.split('/')
    prefix = f"../../../audio-video/{month}/{dirname}/"
    eaf = parse_eaf(ep)
    media_descriptors = get_media_descriptors(eaf)
    for md in media_descriptors:
        fbase = os.path.basename(md.attrib["MEDIA_URL"])
        if fbase.endswith('.mp4'):
            f = f"{prefix}{fbase}"
        else:
            f = f"{prefix}{fbase[:-4]}.wav"
        md.attrib["MEDIA_URL"] = f
        md.attrib["RELATIVE_MEDIA_URL"] = f
    return eaf




def main(args):
    eaf_paths = sorted(list(eaf_iterator(tx_dir="mmep-corpus/transcribed-audio", start=args.start, end=args.end)))
    for ep in tqdm(eaf_paths, total=len(eaf_paths)):
        write_eaf(reset_media_descriptors(ep), ep)




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument("-s", "--start", type=int, default=200809, help="Start: YYYYMM")
    parser.add_argument("-e", "--end", type=int, default=201005, help="End: YYYYMM")
    args = parser.parse_args()
    main(args)
