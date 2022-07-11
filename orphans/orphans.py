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
