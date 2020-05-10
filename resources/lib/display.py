# -*- coding: utf-8 -*-

import os
import sys
from traceback import print_exc

from kodi_six import xbmc, xbmcaddon, xbmcgui, xbmcvfs
import urllib2, urllib

#from main import sr_launch as SR_Launch

    
__plugin__       = "ShowRom"
__addonID__      = "plugin.video.tvo"
__settings__     = xbmcaddon.Addon(id=__addonID__)

# INITIALISATION CHEMIN RACINE
ROOTDIR = __settings__.getAddonInfo('path')


#get actioncodes from keymap.xml
ACTION_PREVIOUS_MENU = 10


class DisplayMenu( xbmcgui.WindowXMLDialog ):
    def __init__( self, *args, **kwargs ):
        xbmcgui.WindowXMLDialog.__init__( self, *args, **kwargs )
        print args
        print kwargs
        self.listConsoles = kwargs['consoles']
        self.menuStyle = kwargs['style']
        self.logoRegionList = ['eu','us','jp']
        self.logoRegion = self.logoRegionList[int(kwargs['logoRegion'])]
        self.skinDir = os.path.join(args[1].decode('utf-8'),'resources','skins',args[2])
        self.submenuId = 'exit'
 
    def onInit(self):
    
      #Language :
      self.Language = __settings__.getLocalizedString

      #Controls :

      #self.ctrlDisplayName = self.getControl(2)
      #self.ctrlBirthday = self.getControl(3)
      #self.ctrlImg = self.getControl(20)
      
      self.ctrlListMenu = self.getControl(250)

      #Set info :
      #self.ctrlDisplayName.setLabel( self.displayName(self.contactInfos[2],self.contactInfos[1],self.contactInfos[3]) )
      #self.ctrlBirthday.setLabel( self.contactInfos[6] )
      
      #Set image :
      #urlImg = os.path.join(self.urlImgDir,str(self.contactInfos[7]))
      
      #if os.path.exists(urlImg) and self.contactInfos[7] !="":
      #  self.ctrlImg.setImage(urlImg)
        
      #Menu :
      self.populateConsoles(self.listConsoles,self.ctrlListMenu)
      #Mail :
      #self.populateCtrlList(self.contactMails,self.ctrlListMails, "Mails")
      #Adresses :
      #self.populateCtrlList(self.contactAdresses,self.ctrlListAdresses, "Addresses")

      #self.ctrlOk.setLabel( self.Language(1000) )
            
    def onAction(self, action):
        #Close the script
        
        if action == ACTION_PREVIOUS_MENU :
            self.close()
        
    def onClick(self, controlID):
        """
            Notice: onClick not onControl
            Notice: it gives the ID of the control not the control object
        """
        if controlID == 250 :
            menuPosition = self.ctrlListMenu.getSelectedPosition()
            selectItem =  self.ctrlListMenu.getListItem(menuPosition)
            self.submenuId = selectItem.getLabel()
            self.close()

    
            
  
    def onFocus(self, controlID):
        pass

    def populateConsoles(self, arrConsoles, ctrlList) :
    
      for console in arrConsoles :
          #Media
          pathBackground = os.path.join(self.skinDir,'media','consoles',console['id'],'background.png')
          pathIconRegion = os.path.join(self.skinDir,'media','consoles',console['id'],'logo','logo_%s.png'%(self.logoRegion)) 
          if os.path.exists(pathIconRegion) :
            pathIcon = pathIconRegion  
          else :    
            pathIcon = os.path.join(self.skinDir,'media','consoles',console['id'],'logo.png')    
          #DefaultMedia    
          if not os.path.exists(pathIcon) :
            pathIcon = os.path.join(self.skinDir,'media','consoles','default','logo.png')   
          if not os.path.exists(pathBackground) :
            pathBackground = os.path.join(self.skinDir,'media','consoles','default','background.jpg')
          #create Listitem
          listitem = xbmcgui.ListItem(label=console['id'])
          listitem.setArt({'icon':pathIcon})
          listitem.setArt({'background':pathBackground})
          ctrlList.addItem( listitem )

    def returnSubmenuId(self):
        return self.submenuId

 

class DisplayConsole( xbmcgui.WindowXMLDialog ):
    def __init__( self, *args, **kwargs ):
        xbmcgui.WindowXMLDialog.__init__( self, *args, **kwargs )
        print args
        print kwargs
        self.console = kwargs['console']
        self.listGames = kwargs['games']
        self.menuStyle = kwargs['style']
        self.srMediaDir = kwargs['media']
        self.skinDir = os.path.join(args[1].decode('utf-8'),'resources','skins',args[2])
        print(self.skinDir)
 
    def onInit(self):
    
      #Language :                                          
      self.Language = __settings__.getLocalizedString

      #Controls :

      self.gameList = self.getControl(250)
      #self.ctrlBirthday = self.getControl(3)
      #self.ctrlImg = self.getControl(20)
      
      self.ctrlListGames = self.getControl(250) 

      #Set info :
      #self.ctrlDisplayName.setLabel( self.displayName(self.contactInfos[2],self.contactInfos[1],self.contactInfos[3]) )
      #self.ctrlBirthday.setLabel( self.contactInfos[6] )
      
      #Set image :
      #urlImg = os.path.join(self.urlImgDir,str(self.contactInfos[7]))
      
      #if os.path.exists(urlImg) and self.contactInfos[7] !="":
      #  self.ctrlImg.setImage(urlImg)
        
      #Menu :
      self.populateGames(self.listGames,self.ctrlListGames)
      
            
    def onAction(self, action):
        #Close the script
        
        if action == ACTION_PREVIOUS_MENU :
            self.close()
        
    def onClick(self, controlID):
        """
            Notice: onClick not onControl
            Notice: it gives the ID of the control not the control object
        """
        
        if controlID == 250 : 
            print controlID
            print self.gameList.getSelectedPosition()
            print self.gameList.getSelectedItem()
            print self.gameList.getSelectedItem().getProperty('gameclient')
            #launch_item=SR_Launch()
            launch_item.launch(self.gameList.getSelectedItem())
    
            
  
    def onFocus(self, controlID):
        pass

    def populateGames(self, arrGames, ctrlList) :
    
      for game in arrGames :
          #default art
          if not os.path.exists(game['art']['poster']) :
                game['art']['poster'] = os.path.join(self.skinDir,'media','consoles',game['values']['label2'],'screenshot.png')
          if not os.path.exists(game['art']['landscape']) :
                game['art']['landscape'] = os.path.join(self.skinDir,'media','consoles',game['values']['label2'],'bezel.png')
          if not os.path.exists(game['art']['icon']) :
                game['art']['icon'] = os.path.join(self.skinDir,'media','consoles',game['values']['label2'],'cover.png')
          if not os.path.exists(game['art']['thumb']) :
                game['art']['thumb'] = os.path.join(self.skinDir,'media','consoles',game['values']['label2'],'support.png')
          #rating
          ratingNote = int(game['property']['rating'] * 10)
          ratingPath =   os.path.join(self.skinDir,'media','consoles',game['values']['label2'],'rating','%s.png'%(ratingNote))
          game['info']['ratingpath'] = ratingPath
          #create Listitem
          listitem = xbmcgui.ListItem(label=game['values']['label'],label2=game['values']['label2'])
          listitem.setArt(game['art']) 
          listitem.setInfo('game',game['info'])
          listitem.setProperties(game['property']) 
          ctrlList.addItem( listitem ) 

         


    
