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

def download(url):
    try:
        webFile = urllib.urlopen(url)
        filename = webFile.headers['Content-Disposition'].split('filename=')[-1].split('"')[1]
        localFile = open(settings.download_dir + filename, 'w')
        localFile.write(webFile.read())
    except: 
        try:
            webFile.close()
            localFile.close()
        except: pass
        return False
    
    webFile.close()
    localFile.close()
    return True

def getFilename(url):
    webFile = urllib.urlopen(url)
    try:
        filename = webFile.headers['Content-Disposition'].split('filename=')[-1].split('"')[1]
    except: 
        webFile.close()
        return False
    webFile.close()
    return filename
