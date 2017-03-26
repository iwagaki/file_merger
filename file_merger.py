#!/usr/bin/env python

import os
import shutil
import filecmp
import hashlib

def find_all_files(directory):
    for root, dirs, files in os.walk(directory):
        for f in files:
            yield root, f

            
def copy_without_overwrite(src_dir, src_file, dest_dir):
    src_path = os.path.join(src_dir, src_file)
    body, ext = os.path.splitext(src_file)

    revision_no = 1
    dest_path = os.path.join(dest_dir, src_file)
    print src_path
    
    if os.path.exists(dest_path):
        while True:
            dest_path = os.path.join(dest_dir, "%s_%s%s" % (body, revision_no, ext))
            if not os.path.exists(dest_path):
                break
            revision_no += 1

    shutil.copy(src_path, dest_path)

    
def get_checksum_md5(file_path):
    md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(2048 * md5.block_size), b''):
            md5.update(chunk)
    return md5.hexdigest()



checksum_list = {}

for root, f in find_all_files('PHOTOS/'):
    path = os.path.join(root, f)
    checksum = get_checksum_md5(path)
    if checksum not in checksum_list:
        copy_without_overwrite(root, f, 'MERGED')
        checksum_list[checksum] = path
    else:
        print "Skipped: %s matched %s" % (path, checksum_list[checksum])