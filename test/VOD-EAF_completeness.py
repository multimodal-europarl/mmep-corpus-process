#!/usr/bin/env python3
"""
Test that all media files have a corresponing eaf
"""
from tqdm import tqdm
import os
import pandas as pd
import unittest
import warnings



class MismatchedMediaSetsWarning(Warning):

    def __init__(self, N):
        self.message = f"There are --| {N} |-- media files that don't match eachother on Garcon and Schoenfinkel."

    def __str__(self):
        return self.message




class MissingTranscriptionsWarning(Warning):

    def __init__(self, N):
        self.message = f"There are --| {N} |-- media files that don't have a corresponding transcription."

    def __str__(self):
        return self.message




class Test(unittest.TestCase):

    def get_mediafile_lists(self):
        print("Fetcing media file lists:")
        with open("test/test-IO/file-lists/schoenfinkel_VODUnit-files.txt", 'r') as s:
            s_media = s.readlines()
        with open("test/test-IO/file-lists/garcon_VODUnit-files.txt", 'r') as g:
            g_media = g.readlines()
        s = [_.strip() for _ in s_media]
        schoenfinkel = [_.split('/')[-1] for _ in s]
        g = [_.strip() for _ in g_media]
        garcon = [_.split('/')[-1] for _ in g]
        print("list, media files, unique media files")
        print("garcon", len(garcon), len(list(set(garcon))))
        print("schoenfinkel", len(schoenfinkel), len(list(set(schoenfinkel))))
        print("done")
        return list(set(schoenfinkel)), list(set(garcon))




    def test_compare_media_lists(self):
        print("Testing media file lists are the same:")
        schoenfinkel, garcon = self.get_mediafile_lists()
        not_on_s = [[_, 'schoenfinkel'] for _ in garcon if _ not in schoenfinkel]
        not_on_g = [[_, 'garcon'] for _ in schoenfinkel if _ not in garcon]
        rows = []
        for missing in [not_on_s, not_on_g]:
            if len(missing) > 0:
                rows = rows + missing
        if len(rows) > 0:
            columns = ["file", "missing_from"]
            df = pd.DataFrame(rows, columns=columns)
            # Make sure `_unittest-output/VOD-EAF_completeness` exists locally
            # Test output is not version controlled
            # Uncomment next line for file output when running locally
            #df.to_csv("IO/_unittest-output/VOD-EAF_completeness/server-media-sets.csv", index=False)
            warnings.warn(str(len(df)), MismatchedMediaSetsWarning)
        self.assertEqual(len(rows), 0, df)




    def test_all_media_has_transcription(self):
        print("Testing all media files have a corresponding transcriptoin file:")
        media = set()
        rows = []
        schoenfinkel, garcon = self.get_mediafile_lists()
        for l in [schoenfinkel, garcon]:
            [media.add(_) for _ in l if _ not in media]
        for m in tqdm(media, total=len(media)):
            m_dirname = m.split("_")[1][:6]
            m_basename = m.split(".")[0]
            m_dirname = m.split("_")[1][:6]
            eaf = f"mmep-corpus/transcribed-audio/{m_dirname}/{m_basename}/{m_basename}.eaf"
            if not os.path.exists(eaf):
                rows.append([m_dirname, m_basename, eaf])
        if len(rows) > 0:
            columns = ["direcrtory", "basename", "eaf_path"]
            df = pd.DataFrame(rows, columns=columns)
            # Make sure `_unittest-output/VOD-EAF_completeness` exists locally
            # Test output is not version controlled
            # Uncomment next line for file output when running locally
            #df.to_csv("IO/_unittest-output/VOD-EAF_completeness/media-without-transcriptions.csv", index=False)
            warnings.warn(str(len(df)), MissingTranscriptionsWarning)
        self.assertEqual(len(rows), 0, df)




if __name__ == '__main__':
    unittest.main()
