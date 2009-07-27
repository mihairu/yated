#!/usr/bin/env python
# -*- coding: utf-8 -*-

########## IMPORT

# nacteni RSS parseru
try:
    import feedparser
except ImportError:
    print 'Module `feedparser` not found. This module is needed for script running.'
    exit('Program terminated.')

import series_handle as handle
import settings as settings
    
########## SETTINGS
# RSS feed - now can handle only show_name
rss_feed = 'http://www.mininova.org/rss/SHOW_NAME/CATEGORY'

categories = ['anime'    : 1,
              'tv_shows' : 8]

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

        exists = False
        settings.shows_cache = handle.file_get_series_cache(settings.file_series_cache)
        for tmp in settings.shows_cache:
            # is show in shows_cache?
            if(handle.show_to_search(show_name).lower() == tmp['show_name']):
                exists = True

        if exists == False:
            handle.file_save_series_cache(settings.file_series_cache, handle.show_to_search(show_name).lower())
            settings.shows_cache = handle.file_get_series_cache(settings.file_series_cache)

        for tmp in settings.shows_cache:
            if(handle.show_to_search(show_name).lower() == tmp['show_name']):
                # search for all episodes in same or newer season
                if int(show_season) >= int(tmp['show_season']):
                    # search for newer episodes in same season
                    if int(show_season) == int(tmp['show_season']) and int(show_episode) > int(tmp['show_episode']):
                        data = handle.show_to_search(show_name).lower(), show_season, show_episode, show_url_from, show_url
                        handle.file_save_series_download(settings.file_series_torrent, data)

                    # search for all episodes in newer season
                    if int(show_season) > int(tmp['show_season']):
                        data = handle.show_to_search(show_name).lower(), show_season, show_episode, show_url_from, show_url
                        handle.file_save_series_download(settings.file_series_torrent, data)

def get_feeds():
    ### init of shows
    shows = handle.file_get_series(settings.file_series)
    shows_cache = handle.file_get_series_cache(settings.file_series_cache)

    ### delete download file
    handle.file_delete_series_download(settings.file_series_torrent)

    for show in shows:
        to_search = handle.show_to_search(show)
        feed = feed_check(to_search)
        feed_parse(feed)

    return True
