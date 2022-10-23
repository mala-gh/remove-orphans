# remove-orphans

This is a tool to support the handling of RAW and JPEG files. Since modern cameras can produce both at the same time, but photo library tools (e.g. Lightroom) only import either the RAW or the JPEG, you are bound to encounter orphans (a RAW file without a JPEG) if you review your library and afterwards only delete one of the corrsponding files (e.g. only the JPEG). 

This tool looks through the RAW directory, and moves (or deletes) every RAW file which does not have a corresponding JPEG. The comparison is made solely on the file name, not on the relative path in the respective directory.

The other way around (delete JPEGs which do not have a corresponding RAW) is not supported at the moment, but might be in the future.

## Command line interface
```
usage: orphans_cli.py [-b BACKUP_FOLDER] RAW_folder JPG_folders [JPG_folders ...]
```

Moves all RAW files to the BACKUP_FOLDER, if there is no corrersponding JPEG in the JPEG_folders

## Graphical user interface

![orphans_cli](https://user-images.githubusercontent.com/108183428/179416108-4686cea6-74fd-452c-9fc9-223583624029.png)

Moves all RAW files to the BACKUP_FOLDER, if there is no corrersponding JPEG in the JPEG_folders
