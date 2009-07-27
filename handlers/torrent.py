#!/usr/bin/env python
# -*- coding: utf-8 -*-

########## IMPORT

# nacteni urllib
try:
    import urllib
except ImportError:
    print 'Module `urllib` not found. This module is needed for script running.'
    exit('Program terminated.')

import settings as settings

class TorrentDownload():
    def __init__(self, url):
        self.url = url
        self.remoteFile = urllib.urlopen(self.url)
        self.fetchFilename()
        self.createLocalFileHandler()

    def __del__(self):
        self.remoteFile.close()
        self.localFile.close()

    def start(self):
        try:
            self.localFile.write(self.remoteFile.read())
        except: 
            return False
        return True

    def fetchFilename(self):
        try:
            self.filename = self.remoteFile.headers['Content-Disposition'].split('filename=')[-1].split('"')[1]
        except: 
            return False
        return True

    def createLocalFileHandler(self):
        try:
            self.localFile = open(settings.download_dir + self.filename, 'w')
        except:
            return False
        return True
