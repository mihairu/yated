#!/usr/bin/env python
# -*- coding: utf-8 -*-

########################:about:##########################
# Author: Michal Orlik                                  #
# Version: 0.3                                          #
# Description: CLI-version of client for series fetcher #
#########################################################

############ IMPORT
import fetchers.tvrss_fetch as tvrss

import settings as settings
#import series_handle as handle

import handlers.c_torrent as c_torrent
import handlers.c_sqlite as c_sqlite

import sys
from optparse import OptionParser

sqlite_h = c_sqlite.SQLiteHandler()

width = 40
VERSION = '0.3'

parser = OptionParser(epilog=""" yated (Yet Another Torrent Episode Downloader) %s - CLI-CLIENT
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~""" % VERSION, 
usage="\n\t%prog [options]", version="%%prog %s" % VERSION)
parser.add_option("--add", action="store_true", dest="ADD", default=False,
                  help="add new serie")
parser.add_option("--get", action="store_true",dest="GET", default=False,
                  help="download torrent files")
parser.add_option("--tlist", action="store_true",dest="TORRENTS", default=False,
                  help="get list of torrents")
parser.add_option("--list", action="store_true",dest="LIST", default=False,
                  help="get list of series")
parser.add_option("--check", action="store_true",dest="CHECK", default=False,
                  help="check for new episodes")
(options, argURL) = parser.parse_args()

def get_torrents(download):
    torrents = []

    print 'List of torrents to download:'
    print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
    for x,torrent in enumerate(settings.torrents):
        id = x+1
        print '% 4i)'%id, '\t', torrent['filename']
        torrents.append(torrent)
        
    if download == True:
        print ''
        print u'Enter n~ (separated by blanks or a range) of torrents to be downloaded'
        print 'Example: \'1 2 3 4 5 6\' or \'1-6\''
        key_pressed = raw_input('-> ')
        if (key_pressed == ''):
            exit()
        else:
            print ''
            for x in key_pressed.split(' '):
                downTorrent = torrents[int(x)-1]
                print ' Downloading torrent: ' + torrents[int(x)-1]['filename'],
                torrent_h = c_torrent.TorrentDownload(downTorrent['url'])
                if torrent_h.start():
                    sqlite_h.changeSerie(downTorrent['title'], downTorrent['episode'], downTorrent['season'])
                    sqlite_h.deleteTorrent(downTorrent['filename'])
                    print "\t \033[0;"+str(30+2)+"m"+" DONE \033[0m"
                else:
                    print "\t \033[0;"+str(30+1)+"m"+" !!! FAIL !!! \033[0m"

if options.ADD:
    print 'Add new serie:'
    print '~~~~~~~~~~~~~~'

    title = raw_input('Name of show: ')
    season = raw_input('Fetch from season: ')
    episode = raw_input('Fetch from episode: ')
     
    sqlite_h.addSerie(title, episode, season)


if options.CHECK:
    print 'Checking for new episodes:'
    print '~~~~~~~~~~~~~~~~~~~~~~~~~~'
    sqlite_h.deleteTorrent('all')
    tvrss.get_feeds()

if options.GET:
    get_torrents(True)

if options.TORRENTS:
    get_torrents(False)

if options.LIST:
    print 'List of series:'
    print '~~~~~~~~~~~~~~~'
    for x,serie in enumerate(settings.shows):
        id = x+1 
        new = 0
        for torrent in settings.torrents:
            if (torrent['sid'] == serie['id']):
                new = new + 1
        
        new_width = width-len(serie['title'])
        serie['title'] = serie['title'].ljust(len(serie['title']) + new_width)
        print '% 4i)'%id, '\t', serie['title'] + 'fetch from S%02iE%02i'%(int(serie['season']), int(serie['episode']))
        print '\t\t\t\t\t\t', '%i new episodes'%(new)


try: sys.argv[1]
except: parser.print_help()
