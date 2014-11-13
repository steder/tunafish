"""
$ tunafish <YOUR_LIBRARY_DIRECTORY>

"""

from __future__ import print_function

# TODO: Walk library directory and identify dupes
# TODO: Remove dupes
# TODO: update XML file

from collections import defaultdict
import locale
import os
import pickle
import sys

from acoustid import fingerprint_file
from mutagen import File

LOCALE_ENCODING = locale.getpreferredencoding() or "utf-8"

def main():
    library_dir = os.path.expanduser("~/Music/iTunes/iTunes Media/Music/")
    if len(sys.argv) > 1:
        library_dir = sys.argv[1]

    if not os.path.exists("songs.pickle"):
        mp3_count = 0
        path_count = 0

        mp3_paths = []

        songs = defaultdict(list)

        for root, directories, paths in os.walk(library_dir):
            print(root, directories, paths)
            for path in paths:
                path_count += 1
                if path.endswith(".mp3"):
                    mp3_count += 1
                    full_path = "{}/{}".format(root,path)
                    mp3_paths.append(full_path)
                    length, fingerprint = fingerprint_file(full_path)
                    songs[(length, fingerprint)].append(full_path)

        # print(mp3_paths)
        # for path in mp3_paths:
        #     print(File(path).pprint().encode(LOCALE_ENCODING, 'replace'))
        pickle.dump(songs, open("songs.pickle", "wb"))
        print("Processed {} paths".format(path_count))
        print("Processed {} mp3s".format(mp3_count))

    else:
        songs = pickle.load(open("songs.pickle", "rb"))

    for key in songs:
        if len(songs[key]) > 1:
            print("duplicates:", songs[key])


if __name__=="__main__":
    main()
