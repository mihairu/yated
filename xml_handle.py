#!/usr/bin/env python
# -*- coding: utf-8 -*-

################ TODO ###
######## nacitani xml ###
#########################

# doc = xml.dom.minidom.parse(settings.xml_file) << PRIDAT DO INITU

########## IMPORT
# loading of os module
try:
    import os
except ImportError:
    print 'Module `os` not found. This module is needed for script running.'
    exit('Program terminated.')

try:
    import xml.dom.minidom
    from xml.dom.minidom import Node
except ImportError:
    print 'Module `xml` not found. This module is needed for script running.'
    exit('Program terminated.')

import settings
import sys

def getValue(node, tag):
    return node.getElementsByTagName(tag)[0].childNodes[0].nodeValue

def setValue(node, tag, value):
    node.getElementsByTagName(tag)[0].childNodes[0].nodeValue = value
    return True

def toSearch(title):
    to_search = title.split(' ')
    return '+'.join(to_search).lower()

## LOAD SERIES INFO INTO settings.shows
def getSeries(*args):
    try:
        doc = xml.dom.minidom.parse(settings.xml_file)
    except:
        return False
    
    # "pretizeni funkce" - zjisteni jen jedne serie
    if args:
        title = toSearch(args[0])
        for series in doc.getElementsByTagName("series"):
            for serie in series.getElementsByTagName("serie"):
                if getValue(serie, 'search') == title:
                    show = {'title'       :getValue(serie, 'title'),
                            'episode'     :getValue(serie, 'episode'),
                            'season'      :getValue(serie, 'season'),
                            'fetch_from'  :getValue(serie, 'fetch_from'),
                            'search'      :getValue(serie, 'search')}
                    return show
        return False

    # pokud neni zadan argument
    settings.show = []
    for series in doc.getElementsByTagName("series"):
        for serie in series.getElementsByTagName("serie"):
            show = {'title'       :getValue(serie, 'title'),
                    'episode'     :getValue(serie, 'episode'),
                    'season'      :getValue(serie, 'season'),
                    'fetch_from'  :getValue(serie, 'fetch_from'),
                    'search'      :getValue(serie, 'search')}
            
            settings.shows.append(show)

## LOAD TORRENTS INFO INTO settings.torrents
## nejak lepe poresit ty fory to je otres
def getTorrents():
    try:
        doc = xml.dom.minidom.parse(settings.xml_file)
    except:
        return False

    settings.torrents = []
    for series in doc.getElementsByTagName("series"):
        for serie in series.getElementsByTagName("serie"):
            for torrents in serie.getElementsByTagName("torrents"):
                for tmp in torrents.getElementsByTagName("torrent"):
                    torrent = {'url'        :getValue(tmp, 'url'),
                               'tracker'    :getValue(tmp, 'tracker'),
                               'filename'   :getValue(tmp, 'filename'),
                               'episode'    :getValue(tmp, 'episode'),
                               'season'     :getValue(tmp, 'season'),
                               'title'      :getValue(serie, 'title')}

                    settings.torrents.append(torrent)

def xmlExists():
    try:
        f = open(settings.xml_file,"r")
    except:
        return False

    f.close()
    return True

def torrentExists(torrent):
    getTorrents()
    for _torrent in settings.torrents:
        if torrent['url'] == _torrent['url']:
            return True
        else:
            continue
    return False

### return array of nodes
def createChildArray(values):
    doc = xml.dom.minidom.parse(settings.xml_file)
    out = []
    for key in values:
        value = values[key]
        tmp = doc.createElement(key)
        txt = doc.createTextNode(str(value))
        tmp.appendChild(txt)

        out.append(tmp)
    return out

def appendChildArray(node, childnodes):
    doc = xml.dom.minidom.parse(settings.xml_file)
    for childnode in childnodes:
        node.appendChild(childnode)
    return True

def addTorrent(title, url, tracker, filename, episode, season):
    try:
        if(xmlExists() == False):
            f = open(settings.xml_file,"w")
            _xml = xml.dom.minidom.Document()

            series = _xml.createElement("series")
            _xml.appendChild(series)

            _xml.writexml(f, "    ", "", "\n", "UTF-8")
            f.close()

        doc = xml.dom.minidom.parse(settings.xml_file)
    except:
        return False

    for series in doc.getElementsByTagName("series"):
        for serie in series.getElementsByTagName("serie"):
            if (title == getValue(serie, 'title')):
                # pokud neexistuje torrents
                if len(serie.getElementsByTagName("torrents")) == 0:
                    torrents = doc.createElement("torrents")
                    serie.appendChild(torrents)

                torrents = serie.getElementsByTagName("torrents")[0]
 
                input = {'title'      :title,
                         'episode'    :episode,
                         'season'     :season,
                         'url'        :url,
                         'tracker'    :tracker,
                         'filename'   :filename}

                if (torrentExists(input) == False):
                    # pridavam novy torrent
                    torrent = doc.createElement("torrent")
                    appendChildArray(torrent, createChildArray(input))
                    torrents.appendChild(torrent)

                    #print doc.toprettyxml('     ', '\n', 'utf-8')
                    f = open(settings.xml_file,"w")
                    doc.writexml(f, "", "", "", "UTF-8")
                    f.close()

                #at the end refresh torrents
                getTorrents()
                break
            else:
                continue

def addSerie(title, episode=1, season=1, fetch_from='tvrss'):
    try:
        if(xmlExists() == False):
            f = open(settings.xml_file,"w")
            _xml = xml.dom.minidom.Document()

            series = _xml.createElement("series")
            _xml.appendChild(series)

            _xml.writexml(f, "    ", "", "\n", "UTF-8")
            f.close()

        doc = xml.dom.minidom.parse(settings.xml_file)
    except:
        return False

    series = doc.childNodes[0]
    
    serie = doc.createElement("serie")

    input = {'title'        :title,
             'episode'      :episode,
             'season'       :season,
             'fetch_from'   :fetch_from,
             'search'       :toSearch(title)}

    appendChildArray(serie, createChildArray(input))

    series.appendChild(serie)

    #print doc.toprettyxml('     ', '\n', 'utf-8')
    # TODO - hodit do funkce - opakuje se
    f = open(settings.xml_file,"w")
    doc.writexml(f, "", "", "", "UTF-8")
    f.close()

    # at the end refresh series
    getSeries()

def getSerieNode(title):
    try:
        doc = xml.dom.minidom.parse(settings.xml_file)
    except:
        return False

    title = toSearch(title)
    for series in doc.getElementsByTagName("series"):
        for serie in series.getElementsByTagName("serie"):
            if getValue(serie, 'search') == title:
                return doc,serie

def getTorrentNode(filename):
    try:
        doc = xml.dom.minidom.parse(settings.xml_file)
    except:
        return False

    for series in doc.getElementsByTagName("series"):
        for serie in series.getElementsByTagName("serie"):
            for torrents in serie.getElementsByTagName("torrents"):
                for torrent in torrents.getElementsByTagName("torrent"):
                    return doc,torrent,torrents



def changeSerie(title, episode, season):
    doc,serie = getSerieNode(title)
    _episode = getValue(serie, 'episode')
    _season = getValue(serie, 'season')
    
    if (int(season) == int(_season) and int(episode) > int(_episode)) or int(season) > int(_season):
        #print serie.episode
        setValue(serie, 'episode', episode)
        setValue(serie, 'season', season)
        f = open(settings.xml_file,"w")
        doc.writexml(f, "", "", "", "UTF-8")
        f.close()

def deleteTorrent(filename):
    doc,torrent,node = getTorrentNode(filename)
    node.removeChild(torrent)
    
    f = open(settings.xml_file,"w")
    doc.writexml(f, "", "", "", "UTF-8")
    f.close()
    return True
