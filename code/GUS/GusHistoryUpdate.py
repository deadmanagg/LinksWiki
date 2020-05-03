#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  3 01:03:45 2020

@author: deepansh.aggarwal
"""

import sys
import GUSClient

path = '/Users/deepansh.aggarwal/Study/Projects/LinksWiki/code/chromeHistory/'
if path not in sys.path:
    sys.path.insert(0,path)

import chromeHistoryScrap

import shutil

sourcePath = '/Users/deepansh.aggarwal/Library/Application Support/Google/Chrome/Profile 1/History'

def copyHistoryFile():
    shutil.copy(sourcePath, path)
    return path+"History"


def main():
    filePath = copyHistoryFile()
    chromeHistoryScrap.iterateHistory(filePath)
    GUSClient.iterateGusUrls()
    GUSClient.populateSampleData()

main()
    