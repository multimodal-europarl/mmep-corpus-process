#!/usr/bin/env python3
"""
Create subdirs of mmep-corpus/transcribed audio, so that transcriptions are grouped by year/month.
"""
import os, subprocess




def main():
    os.chdir("mmep-corpus/")
    tx_path = "transcribed-audio/"
    tx_dirs = [_ for _ in os.listdir(tx_path) if _.startswith("VODUnit")]
    for d in  tx_dirs:
        yyyymm = d.split('_')[1][:6]
        if not os.path.isdir(f"{tx_path}{yyyymm}"):
            os.mkdir(f"{tx_path}{yyyymm}")
        subprocess.call(["git", "mv", f"{tx_path}{d}", f"{tx_path}{yyyymm}/{d}"])




if __name__ == '__main__':
    main()
