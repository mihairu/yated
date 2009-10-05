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
import handlers.xml_files as xml

class TorrentDownload():
    def __init__(self, url):
        self.url = url
        self.remoteFile = urllib.urlopen(self.url)
        self.fetchFilename()
        self.createLocalFileHandler()

    def __del__(self):
        try:
            self.remoteFile.close()
            self.localFile.close()
        except:
            pass

    def start(self):
        try:
            self.localFile.write(self.remoteFile.read())
        except: 
            return False
        return True

    def fetchFilename(self):
        self.filename = self.url.split('/')[-1]

    def createLocalFileHandler(self):
        try:
            self.localFile = open(settings.download_dir + self.filename, 'w')
        except:
            return False
        return True

class Torrent():
    def __init__(self):
        pass
    
    def fetchFilename(self, url):
        filename = url.split('/')[-1]
        return filename
