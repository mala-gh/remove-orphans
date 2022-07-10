"""
remove_orphans.py <raw dir> [<JPG dir1> [<JPG dir2> ...]]
Moves raw (NEF/RW2) files in <raw dir> to <raw dir>/raw-orphans  if no corresponding JPG in any of the JPR dirs.
Looks recursively in all the directories.  Creates raw-orphans/ folder if it doesn't already exist.

Examples / Tests :

 remove_orphans.py .
      Lists all NEF/RW2s in current (.) and below dirs.
      Lists all JPEGs in current (.) and below dirs.
      Moves to raw-orphans/ folder all NEF/RW2s without corresponding JPEG.

remove_orphans.py . otherDir
      Lists all NEF/RW2s in current (.) and below dirs.
      Lists all JPEGs in current (.) and below dirs AND in otherDir and below dirs.
      Moves to raw-orphans/ folder all NEF/RW2s without corresponding JPEG.

remove_orphans.py rawDir  JPGDir1 JPGDir2
      Lists all NEF/RW2s in rawDir and below dirs.
      Lists all JPEGs in rawDir and below dirs AND in JPGdir1 and below AND in JPGdir2 and below
      Moves to raw-orphans/ folder all NEF/RW2s without corresponding JPEG.

Verify usage output:
>> print commands.getoutput("python remove_orphans.py")
usage: remove_orphans.py [-h] [-n] [-b BACKUP_FOLDER] [-q] [-t]
                                     RAW_folder
                                     [JPG_folders [JPG_folders ...]]
remove_orphans.py: error: too few arguments

>> print commands.getoutput("python remove_orphans.py -h")
usage: remove_orphans.py [-h] [-n] [-b BACKUP_FOLDER] [-q] [-t]
                                     RAW_folder
                                     [JPG_folders [JPG_folders ...]]
<BLANKLINE>
Cleanup of leftover raw image files (*.RW2 *.NEF).
<BLANKLINE>
positional arguments:
  RAW_folder            Folder tree to check for raw (NEF/RW2) images.
                        Defaults to the current working directory
  JPG_folders           More folder(s) to check for JPGs. (default: None)
<BLANKLINE>
optional arguments:
  -h, --help            show this help message and exit
  -n, --no-backup       Don't back up orphaned raw images - delete them
                        immediately. (default: False)
  -b BACKUP_FOLDER, --backup-folder BACKUP_FOLDER
                        Folder to move orphaned raw images to. (default:
                        raw_orphans)
  -q, --quiet           Silence the less important output of this tool.
                        (default: False)
  -t, --test            Run unit self test in development environment
                        (default: False)

>> shutil.rmtree('testDirs')
>> shutil.copytree('remove_orphaned_raw_images_TestDirs/masterStartDirs/', 'testDirs')

>> print commands.getoutput("python remove_orphans.py TestDirs/01_noPicts")
No images found. No use checking 'TestDirs/01_noPicts' for orphaned RAW images

>> print commands.getoutput("python remove_orphans.py TestDirs/02_jpegNoRaw")
No RAW images found, but 1 JPEGs. Won't do anything now.

>> print commands.getoutput("python remove_orphans.py TestDirs/03_jpgMatchNEF")
1 RAW images found, and 1 JPEGs but no orphans. Won't do anything now.

>> print commands.getoutput("python remove_orphans.py TestDirs/04_NefNoJpeg/")
Moving TestDirs/04_NefNoJpeg/DSC_1381.NEF to TestDirs/04_NefNoJpeg/raw_orphans.
Matched JPEGs: 0,  unMatched JPEGs: 0,  orphaned raw moved: 1

>> print commands.getoutput("python remove_orphans.py TestDirs/05_jpgNotMatchNEF/")
Moving TestDirs/05_jpgNotMatchNEF/DSC_1381.NEF to TestDirs/05_jpgNotMatchNEF/raw_orphans.
Matched JPEGs: 0,  unMatched JPEGs: 1,  orphaned raw moved: 1

>> print commands.getoutput("python remove_orphans.py TestDirs/06_RW2NoJpeg/" )
Moving TestDirs/06_RW2NoJpeg/P1010393.RW2 to TestDirs/06_RW2NoJpeg/raw_orphans.
Matched JPEGs: 0,  unMatched JPEGs: 0,  orphaned raw moved: 1

>> print commands.getoutput("python remove_orphans.py TestDirs/07_jpgMatchRW2/" )
1 RAW images found, and 1 JPEGs but no orphans. Won't do anything now.

>> print commands.getoutput("python remove_orphans.py testDirs/08_DupNefs/" )
'testDirs/08_DupNefs/DSC_1380.NEF' is a duplicate file
Moving testDirs/08_DupNefs/subFolder/DSC_1380.NEF to testDirs/08_DupNefs/raw_orphans.
Matched JPEGs: 0,  unMatched JPEGs: 0,  orphaned raw moved: 1

>> print commands.getoutput("python remove_orphans.py TestDirs/09_RawOnly TestDirs/09_jpegOnly" )
'TestDirs/09_jpegOnly/P1010415.JPG' is a duplicate file
Moving TestDirs/09_RawOnly/DSC_1380.NEF to TestDirs/09_RawOnly/raw_orphans.
Matched JPEGs: 3,  unMatched JPEGs: 1,  orphaned raw moved: 1

>> print commands.getoutput("python remove_orphans.py TestDirs/10_jpgExtraNEF/" )
Moving TestDirs/10_jpgExtraNEF/DSC_1380.NEF to TestDirs/10_jpgExtraNEF/raw_orphans.
Matched JPEGs: 1,  unMatched JPEGs: 0,  orphaned raw moved: 1

>> print commands.getoutput("python remove_orphans.py TestDirs/11_jpgsExtraRW2s/" )
Moving TestDirs/11_jpgsExtraRW2s/P1010416.RW2 to TestDirs/11_jpgsExtraRW2s/raw_orphans.
Moving TestDirs/11_jpgsExtraRW2s/P1010417.RW2 to TestDirs/11_jpgsExtraRW2s/raw_orphans.
Matched JPEGs: 2,  unMatched JPEGs: 0,  orphaned raw moved: 2

>> print commands.getoutput("python remove_orphans.py TestDirs/12_jpgsExtraSubDirNEF+RW2s/" )
Moving TestDirs/12_jpgsExtraSubDirNEF+RW2s/12_jpgsExtraSubDirNEF+RW2sNEF/DSC_1380.NEF to TestDirs/
2_jpgsExtraSubDirNEF+RW2s/raw_orphans.
Moving TestDirs/12_jpgsExtraSubDirNEF+RW2s/12_jpgsExtraSubDirNEF+RW2sRW2/P1010416.RW2 to TestDirs/
12_jpgsExtraSubDirNEF+RW2s/raw_orphans.
Moving TestDirs/12_jpgsExtraSubDirNEF+RW2s/12_jpgsExtraSubDirNEF+RW2sRW2/P1010417.RW2 to TestDirs/
12_jpgsExtraSubDirNEF+RW2s/raw_orphans.
Matched JPEGs: 3,  unMatched JPEGs: 0,  orphaned raw moved: 3

>> print commands.getoutput("python remove_orphans.py -q TestDirs/13_MixedDirRaw testDirs/13_MixedDirRawJPGs
testDirs/13_MixedDirJPGs testDirs/13_MixedDirMoreJPGs" )
'testDirs/13_MixedDirMoreJPGs/DSC_1388.JPG' is a duplicate file
Matched JPEGs: 8,  unMatched JPEGs: 3,  orphaned raw moved: 14

Adapted from  2012-12-12 by Philipp Klaus <philipp.l.klaus →AT→ web.de>.
Check <https://gist.github.com/4271012> for newer versions.

"""

import argparse
import os
import errno
import re
import shutil
import sys
import collections


def stderr(line):
    sys.stderr.write(line + '\n')
    sys.stderr.flush()


def delete(files, backup_folder=None, verbose=True):
    for filename in files:
        if backup_folder:
            if verbose:
                print(f"Moving {filename} to {backup_folder}.")
            shutil.move(filename, os.path.join(backup_folder))
        else:
            if verbose:
                print(f"Deleting {filename}.")
            os.remove(filename)


def listFullNamesFilesInTree(top):
    full_names = []
    for root, dirs, files in os.walk(top, topdown=False):
        for name in files:
            full_names.append(os.path.join(root, name))
    return full_names


def moveOrphans(rawFolder: str, jpegFolder: list, backupDir: str = None, verbose: bool = True):
    raw_images = []

    # Collect all names from all subdirectories.
    raw_files = listFullNamesFilesInTree(rawFolder)

    # there could be JPEGs even in the raw directories
    jpg_files = raw_files
    if isinstance(jpegFolder, str):
        jpg_files = listFullNamesFilesInTree(jpegFolder)
    else:
        for dirName in jpegFolder:
            jpg_files += listFullNamesFilesInTree(dirName)

    # list of bare names (without path) to be able to identify duplicate items
    raw_images_bare_names = []
    # sort files into raw and jpeg files
    for filename in raw_files:
        # The file name of raw image ends with .RW2 for Lumix and .NEF for Nikon
        if re.match(r'(.*)\.(rw|nef|raf)$', filename, re.IGNORECASE):
            basename = os.path.splitext(os.path.basename(filename))[0]
            if basename in raw_images_bare_names:
                stderr(f"{filename!r} is a duplicate raw file")
            else:
                raw_images_bare_names.append(basename)
                raw_images.append(filename)

    # list of bare names (without path) to be able to identify duplicate items
    jpeg_images_bare_names = []
    # Check names only, not directories.
    for filename in jpg_files:
        if re.match(r'(.*)\.jp(e)?g$', filename, re.IGNORECASE):
            basename = os.path.splitext(os.path.basename(filename))[0]
            if basename in jpeg_images_bare_names:
                stderr(f"{filename!r} is a duplicate jpeg file")
            else:
                jpeg_images_bare_names.append(basename)

    # Check if each raw has a corresponding jpeg
    orphans = []
    for raw_image in raw_images:
        if os.path.splitext(os.path.basename(raw_image))[0] not in jpeg_images_bare_names:
            orphans.append(raw_image)

    if backupDir:
        try:
            os.mkdir(backupDir)
        except OSError as e:
            if not e.errno == errno.EEXIST:
                raise

    delete(orphans, backup_folder=backupDir, verbose=verbose)
    matched_jpegs = len(raw_images) - len(orphans)

    Result = collections.namedtuple("Result", ["rawTotal", "rawMoved", "jpegTotal", "jpegUnmatched"])
    return Result(len(raw_images), len(orphans), len(jpeg_images_bare_names), matched_jpegs)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Cleanup of leftover raw image files (*.RW2 *.NEF *.RAF).',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-n', '--no-backup', action='store_true',
                        help='Don\'t backup orphaned raw images - delete them immediately.')
    parser.add_argument('-b', '--backup-folder', default='raw_orphans',
                        help='Folder to move orphaned raw images to.')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='Silence the less important output of this tool.')
    parser.add_argument('raw_folder', metavar='RAW_folder',
                        help='Folder tree to check for RAW images.')
    parser.add_argument('jpg_folders', metavar='JPG_folders', nargs='*',
                        help='More folder(s) to check for JPGs. ')
    args = parser.parse_args()
    verbose = not args.quiet
    backup_folder = None if args.no_backup else args.backup_folder

    moveResult = moveOrphans(args.raw_folder, args.jpg_folders, backup_folder, verbose)

    print(f"total RAWs:         {moveResult.rawTotal:4d}\n"
          f"matched JPEGs:      {(moveResult.jpegTotal - moveResult.jpegUnmatched):4d}\n"
          f"unmatched JPEGs:    {moveResult.jpegUnmatched:4d}\n"
          f"orphaned RAW moved: {moveResult.rawMoved:4d}")