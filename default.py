# Modules
from kodi_six import xbmc, xbmcaddon, xbmcplugin, xbmcgui, xbmcvfs

try:
    from urllib.parse import quote_plus as url_quote
    from urllib.parse import unquote_plus as url_unquote

    xbmc.log(msg='SR:  Using python 3 urrlib', level=xbmc.LOGDEBUG)
except:
    from urllib import quote_plus as url_quote
    from urllib import unquote_plus as url_unquote

    xbmc.log(msg='SR:  Using python 2 urrlib', level=xbmc.LOGDEBUG)

# Modules Perso
from resources.lib.main import *

## Plugin Init##
# script constants
__addon__ = xbmcaddon.Addon()
__addonID__ = __addon__.getAddonInfo('id')
__addonname__ = __addon__.getAddonInfo('name')
__author__ = __addon__.getAddonInfo('author')
__version__ = __addon__.getAddonInfo('version')
__localize__ = __addon__.getLocalizedString
__addonpath__ = __addon__.getAddonInfo('path')
__credits__ = ""
__platform__ = "Kodi, [LINUX, OS X, WIN32]"
__date__ = "05-01-2020"
__settings__ = xbmcaddon.Addon(id=__addonID__)
# Main
SR = sr_utils(name=__addonID__)



# Variables
submenu_id = ''
arr_consoles = list_Consoles(SR.setting_rom_path)

while submenu_id != 'exit' :
    submenu_id = SR.display_Main_Menu(arr_consoles, SR.setting_style_menu, SR.setting_region)
    print(submenu_id)
    print(arr_consoles)
    for dict_console in arr_consoles :
        if submenu_id == dict_console['id'] :
            arr_games = list_Games(SR.rom_Dir(), submenu_id, SR.setting_media_dir)
            SR.display_Console(arr_games, SR.setting_style_game, SR.setting_media_dir, submenu_id)