import shutil

shutil.rmtree('wdir')
shutil.copytree('wdir-orig', "wdir/")
