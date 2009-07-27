#!/usr/bin/env python
# -*- coding: utf-8 -*-

########## IMPORT

# nacteni RSS parseru
try:
    import feedparser
except ImportError:
    print 'Module `feedparser` not found. This module is needed for script running.'
    exit('Program terminated.')

#import series_handle as handle
import xml_handle as xml
import settings as settings
import torrent_down as torrent
    
########## SETTINGS
# RSS feed - now can handle only show_name
rss_feed = 'http://tvrss.net/search/index.php?distribution_group=combined&show_name=SHOW_NAME&show_name_exact=true&filename=&date=&quality=&release_group=&mode=rss'

######### FUNCTIONS
# check feed
def feed_check(show_name):
    tmp = rss_feed.split('SHOW_NAME')
    return feedparser.parse(show_name.join(tmp))

# parse feed
def feed_parse(feed):
    for show in feed['entries']:
        summary = show['summary']

        show_url = show['link']
        show_info = summary.split("; ");

        # parse show data
        for info in show_info:
            if info.startswith("Show Name: "):
                show_name = info.split("Show Name: ")[1]

            if info.startswith("Show Title: "):
                show_title = info.split("Show Title: ")[1]

            if info.startswith("Season: "):
                show_season = info.split("Season: ")[1]

            if info.startswith("Episode: "):
                show_episode = info.split("Episode: ")[1]

        # get show_url_from
        show_url_from = show_url.split('http://')[1].split('/')[0]

        ### show values
        # show_name, show_url, show_url_from, show_title -- always
        # show_season, show_episode -- sometimes
        try: show_season
        except NameError: show_season = 'n/a'

        try: show_episode
        except NameError: show_episode = 'n/a'

        serie = xml.getSeries(show_name)

        # search for all episodes in same or newer season
        if int(show_season) >= int(serie['season']):
            # TODO - DA SE DAT DO JEDNOHO IF
            # search for newer episodes in same season
            if int(show_season) == int(serie['season']) and int(show_episode) > int(serie['episode']) \
            and torrent.getFilename(show_url):
                xml.addTorrent(show_name, show_url, show_url_from, 
                               torrent.getFilename(show_url), show_episode, show_season) 
                
            # search for all episodes in newer season
            if int(show_season) > int(serie['season']) \
            and torrent.getFilename(show_url):
                xml.addTorrent(show_name, show_url, show_url_from,
                               torrent.getFilename(show_url), show_episode, show_season)

def get_feeds():
    ### init of shows
    xml.getSeries()

    for show in settings.shows:
        feed_parse(feed_check(show['search']))

    return True
