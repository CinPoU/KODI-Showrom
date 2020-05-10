import xbmc, xbmcaddon, xbmcplugin, xbmcgui

from resources.lib.display import *
from resources.lib.rbreader import *

class sr_utils(object):
    def __init__(self,**kwargs):
        self.name = kwargs['name']
        self.handle = xbmcaddon.Addon(id='%(addon_name)s' % {'addon_name':self.name})
        self.kodi_version = xbmc.getInfoLabel('System.BuildVersion')
        self.kodi_username = xbmc.getInfoLabel('System.ProfileName')
        self.root_path = self.handle.getAddonInfo('path')
        self.listitem_date_format = '%d/%m/%Y'  #Must be length of 10
        self.display_date_format = '%x'  #Match locale date format by default
        #Settings
        while not self.handle.getSetting("sr_setting_roms_path"):
            self.handle.openSettings()
        self.setting_rom_path = self.handle.getSetting("sr_setting_roms_path")
        self.setting_media_dir = self.handle.getSetting("sr_setting_media_dir")
        self.setting_region = self.handle.getSetting("sr_setting_region")
        self.setting_style_menu = self.handle.getSetting("sr_setting_style_menu")
        self.setting_style_game = self.handle.getSetting("sr_setting_style_game")
        self.setting_history = self.handle.getSetting("sr_setting_history")
        self.setting_show_favs = self.handle.getSetting("sr_setting_show_favs")
        self.setting_autoplay_trailer = self.handle.getSetting("sr_setting_autoplay_trailer")
        #Variables
        self.submenuId = 'exit'

	def loc_str(self,string_id_in):
		try:
			return self.handle.getLocalizedString(string_id_in)
		except:
			xbmc.log(msg='SR Error:  No translation available for %(string_id_in)s' % {'string_id_in': string_id_in}, level=xbmc.LOGERROR)
			return ''

	def initialize_SR_settings(self):
		if self.handle.getSetting(id='sr_external_user_external_env') ==  'Select':  #Not yet defined, try and define for the user
			current_OS = xbmc.getInfoLabel('System.OSVersionInfo')
			xbmc.log(msg='SR:  OS found - %(current_OS)s' % {'current_OS': current_OS}, level=xbmc.LOGDEBUG)
			if 'OS X' in current_OS:
				self.handle.setSetting(id='sr_external_user_external_env',value='OSX')
				xbmc.log(msg='SR:  External Launch Environment auto selected to OSX', level=xbmc.LOGDEBUG)
			elif 'Windows' in current_OS:
				self.handle.setSetting(id='sr_external_user_external_env',value='Windows')
				xbmc.log(msg='SR:  External Launch Environment auto selected to Windows', level=xbmc.LOGDEBUG)
			elif 'Android' in current_OS:
				self.handle.setSetting(id='sr_external_user_external_env',value='Android')
				xbmc.log(msg='SR:  External Launch Environment auto selected to Windows', level=xbmc.LOGDEBUG)
			elif 'Linux' in current_OS:
				self.handle.setSetting(id='sr_external_user_external_env',value='Linux/Kodibuntu')
				xbmc.log(msg='SR:  External Launch Environment auto selected to Linux/Kodibuntu', level=xbmc.LOGDEBUG)				
			else:
				xbmc.log(msg='SR:  External Launch Environment is unknown', level=xbmc.LOGDEBUG)

		if self.handle.getSetting(id='sr_external_user_external_env') in ['OSX','Windows','Linux/Kodibuntu']:  #External environment defined, try and find location of retroarch external app
			if len(self.handle.getSetting(id='sr_external_path_to_retroarch'))<1:
				# possible_retroarch_app_locations = [os.path.join('/Applications','RetroArch.app','Contents','MacOS','RetroArch'),os.path.join('usr','bin','retroarch'),os.path.join('C:','Program Files (x86)','Retroarch','retroarch.exe')]
				pral_found = None
				for pral in self.possible_retroarch_app_locations:
					if xbmcvfs.exists(pral):
						self.handle.setSetting(id='sr_external_path_to_retroarch',value=pral)
						pral_found = pral
				if pral_found is not None:
					xbmc.log(msg='SR:  External Retroarch location defined to %(pral_found)s' % {'pral_found': pral_found}, level=xbmc.LOGDEBUG)
				else:
					xbmc.log(msg='SR:  External Retroarch location is unknown', level=xbmc.LOGDEBUG)

		self.make_scripts_executable() #Attempt to chmod scripts, possibly find a way to only do this once

		# possible_retroarch_config_locations = [os.path.join('mnt','internal_sd','Android','data','com.retroarch','files','retroarch.cfg'),os.path.join('sdcard','Android','data','com.retroarch','files','retroarch.cfg'),os.path.join('data','data','com.retroarch','retroarch.cfg'),os.path.join('data','data','com.retroarch','files','retroarch.cfg')]

	def get_addon_install_path(self):
		return xbmc.translatePath(self.handle.getAddonInfo('path')).decode('utf-8')

	def get_addon_userdata_path(self):
		return xbmc.translatePath(self.handle.getAddonInfo('profile')).decode('utf-8')

	def get_temp_cache_path(self):
		current_path = os.path.join(self.get_addon_userdata_path(),self.temp_cache_folder_name)

		if not xbmcvfs.exists(os.path.join(current_path,'')):
			if not xbmcvfs.mkdir(current_path):
				xbmc.log(msg='SR Error:  Unable to create temp_cache_path', level=xbmc.LOGERROR)

    def rom_Dir(self):
        return self.setting_rom_path
        
    def media_Dir(self):
        return self.setting_media_dir

    def display_Main_Menu(self,consoleList, listStyle, region):
        w = DisplayMenu("hMenu.xml", self.root_path, 'Default', '1080i', consoles=consoleList, style=listStyle,
						logoRegion=region)
        w.doModal()
        self.submenuId = w.returnSubmenuId()
        del w
        return self.submenuId

    def display_Console(self,gameList, listStyle, mediaDir, consoleId):
        w = DisplayConsole("hGame.xml", self.root_path, 'Default', '1080i', games=gameList, style=listStyle,
						   media=mediaDir, console=consoleId)
        w.doModal()
        del w
        
    

class sr_launch(object):
	def __init__(self):
		#self.SR = sr_utils() #SR utils Class
		#self.json = None
		self.launcher = 'retroplayer'
		#self.external_launch_command = None
		#self.launch_success = None #Default to unknown successfull launch
		#self.game_id = game_id_in
		#try:
		#	self.json = json.loads(json_in)
		#except Exception as exc: #except Exception, (exc):
		#	self.json = None
		#	xbmc.log(msg='SR Error:  JSON data is not available for launcher.  Exception %(exc)s' % {'exc': exc}, level=xbmc.LOGERROR)

		#if self.json is not None:
		#	self.game_list_id = self.json.get('emu').get('game_list_id')
		#	self.launcher = self.json.get('emu').get('emu_launcher')
		#	self.external_launch_command = self.json.get('emu').get('emu_ext_launch_cmd')
		#	if self.json.get('game').get('rom_override_cmd') is not None and len(self.json.get('game').get('rom_override_cmd'))>0:
		#		self.external_launch_command = self.json.get('game').get('rom_override_cmd')
		#	if self.external_launch_command is not None:
		#		self.external_launch_command = self.SR.get_external_command(self.external_launch_command)
		#if type(filenames_in) is str or type(filenames_in) is unicode:
		#	self.launch_filenames = [filenames_in]
		#else:
		#	self.launch_filenames = filenames_in
		pass

	def launch(self,game_listitem):
		if self.launcher.lower() == 'retroplayer':
			self.launch_success = self.launch_retroplayer(game_listitem)
		#if self.launcher.lower() == 'external':
		#	if self.SR.handle.getSetting(id='sr_external_user_external_env') == 'Android' or self.SR.handle.getSetting(id='sr_external_user_external_env') == 'Android Aarch64':
		#		self.launch_success = self.launch_external_android()
		#	else:
		#		self.launch_success = self.launch_external()
		#if self.launch_success:
			#self.SR.add_game_to_history(self.json,self.game_list_id,self.game_id)

	def launch_retroplayer(self,game_listitem):
		game_url = game_listitem.getProperty('url')
		game_client = game_listitem.getProperty('gameclient')
		if xbmc.Player().isPlaying():
			xbmc.Player().stop()
			xbmc.sleep(500) #If sleep is not called, Kodi will crash - does not like playing video and then swiching to a game
		try:
			xbmc.log(msg='SR:  Gameclient for Retroplayer set to: %(game_client)s' % {'game_client': game_client}, level=xbmc.LOGNOTICE)
			xbmc.log(msg='SR:  Attempting to play the following file through Retroplayer: %(url)s' % {'url': game_url}, level=xbmc.LOGNOTICE)
			xbmc.Player().play(xbmc.translatePath(game_url),game_listitem)
			return True
		except Exception as exc: #except Exception, (exc):
			xbmc.log(msg='SR Error:  Attempt to play game failed with exception %(exc)s' % {'exc': exc}, level=xbmc.LOGDEBUG)
			return False

