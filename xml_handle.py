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

class XMLHandler():
    def __init__(self):
        self.doc = self.refreshXML()
        self.getSeries()
        
    def refreshXML(self):
        try:
            return xml.dom.minidom.parse(settings.xml_file)
        except: return False

    def getSearchString(self, title):
        tmp = title.split(' ')
        return '+'.join(tmp).lower()

    # if some argument begins with @, it will be saved into self.elements
    def getElementsRecursive(self, flush, target, *args):
        if flush == True:
            self.elements = ()
            flush = False
            
        for element in target.getElementsByTagName(args[0]):
            try:
                var, args = args[0].split('@')
                self.elements.append(element)
            except:
                pass
            
            try:
                self.getElementsRecursive(cache, element, args[1:])
            except:
                return target.getElementsByTagName(arg)
        print args        

    def getNodeValue(self, node, tag):
        return node.getElementsByTagName(tag)[0].childNodes[0].nodeValue

    def setNodeValue(self, node, tag, value):
        node.getElementsByTagName(tag)[0].childNodes[0].nodeValue = value
        return True

    # Pokud je zadan argument zjisti pouze jednu serii, jinak vsechny
    def getSeries(self, *args):
        self.doc = self.refreshXML()
        
        # "pretizeni funkce" - zjisteni jen jedne serie
        if args:
            title = self.getSearchString(args[0])
            for serie in self.getElementsRecursive(True, self.doc, 'series', 'serie'):
                if self.getNodeValue(serie, 'search') == title:
                    show = {'title'       :self.getNodeValue(serie, 'title'),
                            'episode'     :self.getNodeValue(serie, 'episode'),
                            'season'      :self.getNodeValue(serie, 'season'),
                            'fetch_from'  :self.getNodeValue(serie, 'fetch_from'),
                            'search'      :self.getNodeValue(serie, 'search')}
                    return show
            return False
    
        # pokud neni zadan argument
        settings.show = []
        for serie in self.getElementsRecursive(True, self.doc, 'series', 'serie'):
            show = {'title'       :self.getNodeValue(serie, 'title'),
                    'episode'     :self.getNodeValue(serie, 'episode'),
                    'season'      :self.getNodeValue(serie, 'season'),
                    'fetch_from'  :self.getNodeValue(serie, 'fetch_from'),
                    'search'      :self.getNodeValue(serie, 'search')}
                
            settings.shows.append(show)
        return True

    ## LOAD TORRENTS INFO INTO settings.torrents
    def getTorrents(self):
        self.doc = self.refreshXML()
        
        settings.torrents = []
        for torrent in self.getElementsRecursive(True, self.doc, 'series', '@serie', 'torrents', 'torrent'):
            torrent = {'url'        :self.getNodeValue(tmp, 'url'),
                       'tracker'    :self.getNodeValue(tmp, 'tracker'),
                       'filename'   :self.getNodeValue(tmp, 'filename'),
                       'episode'    :self.getNodeValue(tmp, 'episode'),
                       'season'     :self.getNodeValue(tmp, 'season'),
                       'title'      :self.getNodeValue(self.elements[0], 'title')}

            settings.torrents.append(torrent)
            
    def xmlExists(self):
        try:
            f = open(settings.xml_file,"r")
        except:
            return False
    
        f.close()
        return True

    def torrentExists(self, torrent):
        self.getTorrents()
        for _torrent in settings.torrents:
            if torrent['url'] == _torrent['url']:
                return True
            else:
                continue
        return False

    ### return array of nodes
    def createChildArray(self, values):
        out = []
        for key in values:
            value = values[key]
            tmp = self.doc.createElement(key)
            txt = self.doc.createTextNode(str(value))
            tmp.appendChild(txt)
    
            out.append(tmp)
        return out

    def appendChildArray(self, node, childnodes):
        for childnode in childnodes:
            node.appendChild(childnode)
        return True

    def addTorrent(self, title, url, tracker, filename, episode, season):
        try:
            if(self.xmlExists() == False):
                f = open(settings.xml_file,"w")
                _xml = xml.dom.minidom.Document()
    
                series = _xml.createElement("series")
                _xml.appendChild(series)
    
                _xml.writexml(f, "    ", "", "\n", "UTF-8")
                f.close()
    
            self.doc = self.refreshXML()
        except:
            return False
    
        for serie in self.getElementsRecursive(True, self.doc, 'series', 'serie'):
            if (title == self.getNodeValue(serie, 'title')):
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
                    self.doc.writexml(f, "", "", "", "UTF-8")
                    f.close()

                #at the end refresh torrents
                self.doc = self.refreshXML()
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
            if self.getNodeValue(serie, 'search') == title:
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
    _episode = self.getNodeValue(serie, 'episode')
    _season = self.getNodeValue(serie, 'season')
    
    if (int(season) == int(_season) and int(episode) > int(_episode)) or int(season) > int(_season):
        #print serie.episode
        self.setNodeValue(serie, 'episode', episode)
        self.setNodeValue(serie, 'season', season)
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
