#!/usr/bin/env python
# -*- coding: utf-8 -*-

########## IMPORT
# loading of os module
try:
    import os
except ImportError:
    print 'Module `os` not found. This module is needed for script running.'
    exit('Program terminated.')

try:
    from pysqlite2 import dbapi2 as sqlite
except ImportError:
    print 'Module `pysqlite2` not found. This module is needed for script running.'
    exit('Program terminated.')

import settings
import sys

class SQLiteHandler():
    def __init__(self):
        createTables = self.dbExists()

        self.connection = sqlite.connect(settings.db_file)
        self.cursor = self.connection.cursor()
        if (createTables != True): self.createTables()

        self.getSeries()
        self.getTorrents()

    def getSearchString(self, title):
        tmp = title.split(' ')
        return '+'.join(tmp).lower()

    def addSerie(self, title, episode, season):
        search = self.getSearchString(title)
        self.cursor.execute("INSERT INTO series VALUES(null,?,?,?,?,?)", 
                            (title, episode, season, 'tvrss', search))
        self.connection.commit()

    def changeSerie(self, title, episode, season):
        serie = self.getSeries(title)
        _episode = serie['episode']
        _season = serie['season']

        if (int(season) == int(_season) and int(episode) > int(_episode)) or int(season) > int(_season):
	    search = self.getSearchString(title)
            self.cursor.execute("UPDATE series set episode=?,season=? where search=?",
                                (episode,season,search))
            self.connection.commit()

    def deleteTorrent(self, filename):
        if filename == 'all':
            self.cursor.execute("DELETE FROM torrents")
        else: 
            self.cursor.execute("DELETE FROM torrents WHERE filename=?", (filename,))
        self.connection.commit()

    def getSeries(self, *args):
        if args:
            title = self.getSearchString(args[0])
            self.cursor.execute("SELECT * from series where search='"+title+"'")
        else:
            settings.shows = []
            self.cursor.execute("SELECT * from series")
        
        for serie in self.cursor.fetchall():
            show = {'id'	  :serie[0],
                    'title'       :serie[1],
                    'episode'     :serie[2],
                    'season'      :serie[3],
                    'fetch_from'  :serie[4],
                    'search'      :serie[5]}
            if args: 
                return show
            else:  
                settings.shows.append(show)
        return True

    def getTorrents(self, *args):
        if args:
            title = self.getSearchString(args[0])
            id = self.getSeries(title)['id']
            self.cursor.execute("SELECT * from torrents where sid='"+id+"'")
        else:
            settings.torrents = []
            self.cursor.execute("SELECT * from torrents")
        
        for torrent in self.cursor.fetchall():
            torrent = {'id'         :torrent[0],
                       'sid'        :torrent[1],
                       'tracker'    :torrent[5],
                       'filename'   :torrent[6],
                       'episode'    :torrent[3],
                       'season'     :torrent[4],
                       'title'      :torrent[2],
                       'url'	    :torrent[7]}
            if args: 
                return torrent
            else:  
                settings.torrents.append(torrent)
        return True

    def addTorrent(self, title, url, tracker, filename, episode, season):
        sid = self.getSeries(title)['id']
        try:
            self.cursor.execute("INSERT into torrents VALUES (null, ?, ?, ?, ?, ?, ?, ?)",
                                (sid, title, episode, season, tracker, filename, url)) 
        except:
            pass
        self.connection.commit()

    def dbExists(self):
        try:
            f = open(settings.db_file,"r")
        except:
            return False
    
        f.close()
        return True


    def createTables(self):
        self.cursor.execute('''CREATE TABLE series (
				id INTEGER PRIMARY KEY,
				title VARCHAR(100),
				episode INTEGER,
				season INTEGER,
				fetch_from VARCHAR(20),
				search VARCHAR(150) UNIQUE)''')

        self.cursor.execute('''CREATE TABLE torrents (
				id INTEGER PRIMARY KEY,
				sid INTEGER,
				title VARCHAR(100),
				episode INTEGER,
				season INTEGER,
				tracker VARCHAR(40),
				filename VARCHAR(200) UNIQUE,
				url VARCHAR(300))''')
        
        self.connection.commit()

sql = SQLiteHandler()
