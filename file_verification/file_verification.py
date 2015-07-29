#!/usr/bin/env python
#-*- coding: uf-8 -*-
#
#
#This is a file verification tool with check file's md5sum in folder

__author__ = 'Smilent'


import hashlib
import os


folder_path = '/root/Desktop/py-tools'

def get_file_list(folder_path):
    file_list = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_list.append('%s%s%s', (root, os.sep, file))

    return file_list

def compute_file_md5sum_by_list(file_list):
    

def main():
    print 'main'







if __name__ == '__main__':
    main()