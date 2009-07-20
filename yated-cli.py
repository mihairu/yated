#!/usr/bin/env python
# -*- coding: utf-8 -*-

########################:about:##########################
# Author: Michal Orlik                                  #
# Version: 0.2                                          #
# Description: CLI-version of client for series fetcher #
#########################################################

############ IMPORT
import tvrss_fetch as tvrss
import torrent_down as downloader
import settings as settings
#import series_handle as handle
import xml_handle as xml
import sys

width = 40

def print_help():
    print 'yated (Yet Another Torrent Episode Downloader) 0.2v - CLI-CLIENT'
    print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
    print 'Usage:    yated-cli.py [options]\n'
    print ' --add        to add new serie'
    print ' --help       to print this help'
    print ' --get        download torrent files'
    print ' --getlist    get list of torrents'
    print ' --list       get list of series'
    print ' --fetch      check for new episodes'

def list_print():
    """ Poresit nice vystup """
    xml.getSeries()
    xml.getTorrents()

    print 'List of series to check:'
    print '~~~~~~~~~~~~~~~~~~~~~~~~'
    for x,serie in enumerate(settings.shows):
        id = x+1 
        new = 0
        
        for torrent in settings.torrents:
            if (torrent['title'] == serie['title']):
                new = new + 1
        
        new_width = width-len(serie['title'])
        serie['title'] = serie['title'].ljust(len(serie['title']) + new_width)
        print '% 4i)'%id, '\t', serie['title'] + 'fetch from S%02iE%02i'%(int(serie['season']), int(serie['episode']))
        print '\t\t\t\t\t\t', '%i new episodes'%(new)

def get_torrents(download):
    xml.getTorrents()

    torrents = []

    print 'List of torrents to download:'
    print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
    for x,torrent in enumerate(settings.torrents):
        id = x+1
        print '% 4i)'%id, '\t', torrent['filename']
        torrents.append(torrent)
        
    if download == True:
        print ''
        print u'Enter n° (separated by blanks or a range) of torrents to be downloaded'
        print 'Example: \'1 2 3 4 5 6\' or \'1-6\''
        key_pressed = raw_input('-> ')
        if (key_pressed == ''):
            exit()
        else:
            print ''
            for x in key_pressed.split(' '):
                downTorrent = torrents[int(x)-1]
                print ' Downloading torrent: ' + torrents[int(x)-1]['filename'],
                if downloader.download(downTorrent['url']):
                    xml.changeSerie(downTorrent['title'], downTorrent['episode'], downTorrent['season'])
                    xml.deleteTorrent(downTorrent['filename'])
                    print "\t \033[0;"+str(30+2)+"m"+" DONE \033[0m"
                else:
                    print "\t \033[0;"+str(30+1)+"m"+" !!! FAIL !!! \033[0m"

##### arguments
for arg in sys.argv: 
    if (arg == '--list'):
        list_print()

    if (arg == '--fetch'):
        print('Checking for new episodes...')
        tvrss.get_feeds()

    if (arg == '--get'):
        get_torrents(True)

    if (arg == '--getlist'):
        get_torrents(False)

    if (arg == '--add'):
        title = raw_input('Name of show: ')
        season = raw_input('Fetch from season: ')
        episode = raw_input('Fetch from episode: ')
     
        xml.addSerie(title, episode, season)

    if (arg == '--help'):
        print_help()

try: sys.argv[1]
except: print_help()
