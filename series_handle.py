#!/usr/bin/env python
# -*- coding: utf-8 -*-

################ TODO ###
######## nacitani xml ###
#########################

########## IMPORT
# loading of os module
try:
    import os
except ImportError:
    print 'Module `os` not found. This module is needed for script running.'
    exit('Program terminated.')

import settings as settings

def show_to_search(show):
    to_search = show.split(' ')
    return '+'.join(to_search)

def file_get_series(filename):
    show = []
    f = open(filename)
    for line in f:
        show.append(line.replace('\n', ''))
    f.close()
    return show

def file_get_series_cache(filename):
    show = []
    try:
        f = open(filename)
    except IOError:
        f = open(filename, 'w')
        return show
        
    for line in f:
        serie = {}
        data = line.split(' ')
        serie = {'show_name':data[0].replace('\n', ''),
                 'show_season':data[1].replace('\n', ''),
                 'show_episode':data[2].replace('\n', '')}
        show.append(serie)
    return show

def file_add_series(filename, filename_cache, name):
    f = open(filename, 'a')
    f.write(name + '\n')
    f.close()

    file_save_series_cache(filename_cache, show_to_search(name).lower())
    return True

def file_save_series_cache(filename, data, episode = 1, season = 1):
    f = open(filename, 'a')
    f.write(data + ' ' + season + ' ' + episode + '\n')
    f.close()
    return True
    
def file_save_series_download(filename, data):
    f = open(filename, 'a')
    f.write(' '.join(data))
    f.write('\n')
    f.close()
    return True

def file_resave_series_cache(filename, data):
    shows = file_get_series_cache(filename)
    
    try: os.remove(filename)
    except: return False

    for show in shows:
        if show['show_name'] == data['show_name']:
            show['show_episode'] = data['show_episode']
            show['show_season'] = data['show_season']
        file_save_series_cache(filename, show['show_name'], show['show_episode'], show['show_season'])

    return True

def file_delete_series_download(filename):
    try: os.remove(filename)
    except: return False
    return True

def file_list_series():
    out = []
    shows = file_get_series(settings.file_series)
    shows_cache = file_get_series_cache(settings.file_series_cache)

    ## rescan
    serie_episode_list()

    #print(settings.new_episodes)

    for show in shows:
        for show_cache in shows_cache:
            num = 0
            for episodes in settings.new_episodes:
                if (show_to_search(show).lower() == episodes['show_name'] and settings.download_from == episodes['tracker']):
                    num = num + 1

            if (show_to_search(show).lower() == show_cache['show_name']):
                data = show + ' - fetch from S%02iE%02i'%(int(show_cache['show_season']), int(show_cache['show_episode']))
                if (num > 0):
                    data = data + ' - %i new episodes'%(num)
                out.append(data)
                break
    return out

def serie_episode_list():
    settings.new_episodes = []
    try:
        f = open(settings.file_series_torrent)
    except: return False
    
    for line in f:
        serie = {}
        data = line.split(' ')
        serie = {'show_name':data[0].replace('\n', ''),
                 'show_season':data[1].replace('\n', ''),
                 'show_episode':data[2].replace('\n', ''),
                 'tracker':data[3].replace('\n', ''),
                 'url':data[4].replace('\n', '')}
        settings.new_episodes.append(serie)
