"""
orphans.py <raw dir> [<JPG dir1> [<JPG dir2> ...]]
Moves raw (NEF/RW2) files in <raw dir> to <raw dir>/raw-orphans  if no corresponding JPG in any of the JPR dirs.
Looks recursively in all the directories.  Creates raw-orphans/ folder if it doesn't already exist.

Examples / Tests :

 orphans.py .
      Lists all NEF/RW2s in current (.) and below dirs.
      Lists all JPEGs in current (.) and below dirs.
      Moves to raw-orphans/ folder all NEF/RW2s without corresponding JPEG.

orphans.py . otherDir
      Lists all NEF/RW2s in current (.) and below dirs.
      Lists all JPEGs in current (.) and below dirs AND in otherDir and below dirs.
      Moves to raw-orphans/ folder all NEF/RW2s without corresponding JPEG.

orphans.py rawDir  JPGDir1 JPGDir2
      Lists all NEF/RW2s in rawDir and below dirs.
      Lists all JPEGs in rawDir and below dirs AND in JPGdir1 and below AND in JPGdir2 and below
      Moves to raw-orphans/ folder all NEF/RW2s without corresponding JPEG.

Verify usage output:
>> print commands.getoutput("python orphans.py")
usage: orphans.py [-h] [-n] [-b BACKUP_FOLDER] [-q] [-t]
                                     RAW_folder
                                     [JPG_folders [JPG_folders ...]]
orphans.py: error: too few arguments

>> print commands.getoutput("python orphans.py -h")
usage: orphans.py [-h] [-n] [-b BACKUP_FOLDER] [-q] [-t]
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

>> print commands.getoutput("python orphans.py TestDirs/01_noPicts")
No images found. No use checking 'TestDirs/01_noPicts' for orphaned RAW images

>> print commands.getoutput("python orphans.py TestDirs/02_jpegNoRaw")
No RAW images found, but 1 JPEGs. Won't do anything now.

>> print commands.getoutput("python orphans.py TestDirs/03_jpgMatchNEF")
1 RAW images found, and 1 JPEGs but no orphans. Won't do anything now.

>> print commands.getoutput("python orphans.py TestDirs/04_NefNoJpeg/")
Moving TestDirs/04_NefNoJpeg/DSC_1381.NEF to TestDirs/04_NefNoJpeg/raw_orphans.
Matched JPEGs: 0,  unMatched JPEGs: 0,  orphaned raw moved: 1

>> print commands.getoutput("python orphans.py TestDirs/05_jpgNotMatchNEF/")
Moving TestDirs/05_jpgNotMatchNEF/DSC_1381.NEF to TestDirs/05_jpgNotMatchNEF/raw_orphans.
Matched JPEGs: 0,  unMatched JPEGs: 1,  orphaned raw moved: 1

>> print commands.getoutput("python orphans.py TestDirs/06_RW2NoJpeg/" )
Moving TestDirs/06_RW2NoJpeg/P1010393.RW2 to TestDirs/06_RW2NoJpeg/raw_orphans.
Matched JPEGs: 0,  unMatched JPEGs: 0,  orphaned raw moved: 1

>> print commands.getoutput("python orphans.py TestDirs/07_jpgMatchRW2/" )
1 RAW images found, and 1 JPEGs but no orphans. Won't do anything now.

>> print commands.getoutput("python orphans.py testDirs/08_DupNefs/" )
'testDirs/08_DupNefs/DSC_1380.NEF' is a duplicate file
Moving testDirs/08_DupNefs/subFolder/DSC_1380.NEF to testDirs/08_DupNefs/raw_orphans.
Matched JPEGs: 0,  unMatched JPEGs: 0,  orphaned raw moved: 1

>> print commands.getoutput("python orphans.py TestDirs/09_RawOnly TestDirs/09_jpegOnly" )
'TestDirs/09_jpegOnly/P1010415.JPG' is a duplicate file
Moving TestDirs/09_RawOnly/DSC_1380.NEF to TestDirs/09_RawOnly/raw_orphans.
Matched JPEGs: 3,  unMatched JPEGs: 1,  orphaned raw moved: 1

>> print commands.getoutput("python orphans.py TestDirs/10_jpgExtraNEF/" )
Moving TestDirs/10_jpgExtraNEF/DSC_1380.NEF to TestDirs/10_jpgExtraNEF/raw_orphans.
Matched JPEGs: 1,  unMatched JPEGs: 0,  orphaned raw moved: 1

>> print commands.getoutput("python orphans.py TestDirs/11_jpgsExtraRW2s/" )
Moving TestDirs/11_jpgsExtraRW2s/P1010416.RW2 to TestDirs/11_jpgsExtraRW2s/raw_orphans.
Moving TestDirs/11_jpgsExtraRW2s/P1010417.RW2 to TestDirs/11_jpgsExtraRW2s/raw_orphans.
Matched JPEGs: 2,  unMatched JPEGs: 0,  orphaned raw moved: 2

>> print commands.getoutput("python orphans.py TestDirs/12_jpgsExtraSubDirNEF+RW2s/" )
Moving TestDirs/12_jpgsExtraSubDirNEF+RW2s/12_jpgsExtraSubDirNEF+RW2sNEF/DSC_1380.NEF to TestDirs/
2_jpgsExtraSubDirNEF+RW2s/raw_orphans.
Moving TestDirs/12_jpgsExtraSubDirNEF+RW2s/12_jpgsExtraSubDirNEF+RW2sRW2/P1010416.RW2 to TestDirs/
12_jpgsExtraSubDirNEF+RW2s/raw_orphans.
Moving TestDirs/12_jpgsExtraSubDirNEF+RW2s/12_jpgsExtraSubDirNEF+RW2sRW2/P1010417.RW2 to TestDirs/
12_jpgsExtraSubDirNEF+RW2s/raw_orphans.
Matched JPEGs: 3,  unMatched JPEGs: 0,  orphaned raw moved: 3

>> print commands.getoutput("python orphans.py -q TestDirs/13_MixedDirRaw testDirs/13_MixedDirRawJPGs
testDirs/13_MixedDirJPGs testDirs/13_MixedDirMoreJPGs" )
'testDirs/13_MixedDirMoreJPGs/DSC_1388.JPG' is a duplicate file
Matched JPEGs: 8,  unMatched JPEGs: 3,  orphaned raw moved: 14

Adapted from  2012-12-12 by Philipp Klaus <philipp.l.klaus →AT→ web.de>.
Check <https://gist.github.com/4271012> for newer versions.

"""

import argparse
import orphans


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

    moveResult = orphans.moveOrphans(args.raw_folder, args.jpg_folders, backup_folder, verbose)

    print(f"total RAWs:         {moveResult.rawTotal:4d}\n"
          f"matched JPEGs:      {(moveResult.jpegTotal - moveResult.jpegUnmatched):4d}\n"
          f"unmatched JPEGs:    {moveResult.jpegUnmatched:4d}\n"
          f"orphaned RAW moved: {moveResult.rawMoved:4d}")
