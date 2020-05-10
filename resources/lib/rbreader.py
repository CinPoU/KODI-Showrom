# -*- coding: utf-8 -*-
#Modules
import os
import xml.etree.ElementTree as ET

#Roms Path :
ROMS_PATH = "Y:\\roms"


#Machines List
def list_Consoles(dirGame) :
    itemConsoles = []
    for dirConsole in os.listdir(dirGame) :
        itemConsole = {'id':dirConsole}
        xmlConsoleGames = os.path.join(dirGame,dirConsole,"gamelist.xml")
        if os.path.exists(xmlConsoleGames) :
            itemConsoles.append(itemConsole)
    return itemConsoles


#Games List
def list_Games(dirGame,idConsole,dirMedia) :
    #Define games list
    gameItems = []
    #XML games list
    xmlDir = os.path.join(dirGame,idConsole)
    xmlGames = os.path.join(xmlDir,"gamelist.xml")
    print xmlGames
    if os.path.exists(xmlGames) :
        tree = ET.parse(xmlGames)
        root = tree.getroot()
        for gameNode in root.findall('game') :
            #Define game dictionary
            name = gameNode.findtext("name")
            path = gameNode.findtext("path")[2:]
            url = os.path.join(xmlDir,path) 
            imgName = os.path.splitext(path)
            date = gameNode.findtext("releasedate")
            rating = float(gameNode.findtext("rating"))
            #genres = [x.strip() for x in gameNode.findtext("genre").split(',')]
            if len(date) >= 8 :
                date = '%s-%s-%s'%(date[:4],date[4:6],date[6:8])
            gameItem = {'values' : {
                        'label' : name,
    					'label2' : idConsole,
					},
                    'art' : {
                        'poster' : os.path.join(xmlDir,dirMedia,'screenshot','%s.png'%(imgName[0])),
    					'landscape' : os.path.join(xmlDir,dirMedia,'bezel','%s.png'%(imgName[0])),
    					'fanart' : os.path.join(xmlDir,dirMedia,'fanart','%s.jpg'%(imgName[0])),
    					'clearlogo' : os.path.join(xmlDir,dirMedia,'wheel','%s.png'%(imgName[0])),
    					'icon' : os.path.join(xmlDir,dirMedia,'box3d','%s.png'%(imgName[0])),
    					'thumb' : os.path.join(xmlDir,dirMedia,'support','%s.png'%(imgName[0])),
					},
                    'info' : {
                        'originaltitle' : name,
    					'title' : name,
    					'info' : gameNode.findtext("desc"),
    					'overview' : gameNode.findtext("desc"),
    					'year' : date,
    					'developer' : gameNode.findtext("developer"),
    					'genre' : gameNode.findtext("genre"),
    					#'genres' : genres,
    					'url' : url,
    					'gameclient' : 'game.libretro.snes9x', 
    					#'gameclient' : 'game.libretro.mupen64plus', game.libretro.cap32
                    },
                    'property' : {
                        'originaltitle' : name,
    					'title' : name,
    					'plot' : gameNode.findtext("desc"),
    					'trailer' : gameNode.findtext("video"),
    					'path' : path,
    					'url' : url,
    					'rating' : rating,
    					'dateadded' : date,
    					'writer' : gameNode.findtext("developer"),
    					'studio' : gameNode.findtext("publisher"),
    					'genre' : gameNode.findtext("genre"),
    					'episode' : gameNode.findtext("players"),
    					'playcount' : gameNode.findtext("playcount"),
    					'lastplayed' : gameNode.findtext("lastplayed"),
					}
                }
            gameItems.append(gameItem) 
    return gameItems
    
#for console in list_Consoles(ROMS_PATH) :
#    print console['localTitle']  
#    print list_Games(console['path'])   