#!/usr/bin/env python
# #-*- coding: utf-8 -*-
#
#
#This is a file verification tool with check file's md5sum in folder

__author__ = 'Smilent'


import hashlib
import os

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


folder_path = '/root'

def get_file_list(folder_path):
    file_list = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_list.append('%s%s%s' % (root, os.sep, file))

    return file_list

def compute_file_md5sum_by_list(file_list):
    for file_path in file_list:
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as f:
                m = hashlib.md5()
                while True:
                    data = f.read(8192)
                    if not data:
                        break
                    m.update(data)
                print file_path, m.hexdigest()



def main():
    file_list = get_file_list(folder_path)
    compute_file_md5sum_by_list(file_list)

    observer = Observer()


if __name__ == '__main__':
    main()