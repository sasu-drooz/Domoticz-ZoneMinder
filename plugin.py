# ZoneMinder Python Plugin
#
# Author: zaraki673
# http://zoneminder.readthedocs.io/en/latest/api.html
#
"""
<plugin key="ZoneMinder" name="ZoneMinder Controller plugin" author="zaraki673" version="1.0.1" externallink="http://zoneminder.readthedocs.io/en/stable/api.html">
	<params>
		<param field="Mode1" label="ZM API url" width="150px" required="true"/>
		<param field="Username" label="ZM Login" width="150px" required="false"/>
		<param field="Password" label="ZM Password" width="150px" required="false"/>
		<param field="Mode6" label="Debug" width="75px">
			<options>
				<option label="True" value="Debug"/>
				<option label="False" value="Normal"  default="true" />
			</options>
		</param>
	</params>
</plugin>
"""
import Domoticz
import http.cookiejar, urllib 

class URL:
	
	def __init__(self):
		# On active le support des cookies pour urllib
		cj = http.cookiejar.CookieJar()
		self.urlOpener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
	
	def call(self, url, params = None, referer = None, output = None):
		#Domoticz.Log('Calling url')
		data = None if params == None else urllib.parse.urlencode(params).encode("utf-8")
		request = urllib.request.Request(url, data)
		if referer is not None:
			request.add_header('Referer', referer)
		response = self.urlOpener.open(request)
		Domoticz.Log(" -> %s" % response.getcode())
		return response

class BasePlugin:
	enabled = False
	def __init__(self):
		#self.var = 123
		return

	def onStart(self):
		Domoticz.Log("onStart called")
		if Parameters["Mode6"] == "Debug":
			Domoticz.Debugging(1)
		if (len(Devices) == 0):
			Options = {"LevelActions": "||||","LevelNames": "Start|Stop|Restart","LevelOffHidden": "True","SelectorStyle": "0"}
			Domoticz.Device(Name="Status",  Unit=1, TypeName="Selector Switch", Switchtype=18, Image=12, Options=Options).Create()
			
			Options = {"LevelActions": "|||||||","LevelNames": "None|Monitor|Modect|Record|Mocord|Nodect","LevelOffHidden": "True","SelectorStyle": "0"}
			Domoticz.Device(Name="Monitor 1 Function",  Unit=2, TypeName="Selector Switch", Switchtype=18, Image=12, Options=Options).Create()
			
			Domoticz.Device(Name="Monitor 1 status", Unit=3, Type=17, Switchtype=0).Create()
			Domoticz.Log("Devices created.")
		else:
			if (1 in Devices): conso = Devices[1].nValue
		DumpConfigToLog()
		Domoticz.Heartbeat(60)

	def onStop(self):
		Domoticz.Log("onStop called")

	def onConnect(self, Connection, Status, Description):
		Domoticz.Log("onConnect called")

	def onMessage(self, Connection, Data):
		Domoticz.Log("onMessage called")

	def onCommand(self, Unit, Command, Level, Hue):
		url = URL()	
		Domoticz.Log("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))
		if Unit == 1:
			if Level == 10:
				urlConnect = 'http://'+ Parameters["Mode1"] +'/index.php?username='+ Parameters["Username"] +'&password='+ Parameters["Password"] +'&action=login&view=console'
				url.call(urlConnect)
				urlConnect = 'http://'+ Parameters["Mode1"] +'/api/states/change/start.json'
				url.call(urlConnect)
			
			if Level == 20:
				urlConnect = 'http://'+ Parameters["Mode1"] +'/index.php?username='+ Parameters["Username"] +'&password='+ Parameters["Password"] +'&action=login&view=console'
				url.call(urlConnect)
				urlConnect = 'http://'+ Parameters["Mode1"] +'/api/states/change/stop.json'
				url.call(urlConnect)
			
			if Level == 30:
				urlConnect = 'http://'+ Parameters["Mode1"] +'/index.php?username='+ Parameters["Username"] +'&password='+ Parameters["Password"] +'&action=login&view=console'
				url.call(urlConnect)
				urlConnect = 'http://'+ Parameters["Mode1"] +'/api/states/change/restart.json'
				url.call(urlConnect)

		if Unit == 2:
			if Level == 10:
				urlConnect = 'http://'+ Parameters["Mode1"] +'/index.php?username='+ Parameters["Username"] +'&password='+ Parameters["Password"] +'&action=login&view=console'
				url.call(urlConnect)
				urlConnect = 'http://'+ Parameters["Mode1"] +'/api/monitors/1.json'
				parameters = {'Monitor[Function]' : 'None'}
				url.call(urlConnect, parameters)
			if Level == 20:
				urlConnect = 'http://'+ Parameters["Mode1"] +'/index.php?username='+ Parameters["Username"] +'&password='+ Parameters["Password"] +'&action=login&view=console'
				url.call(urlConnect)
				urlConnect = 'http://'+ Parameters["Mode1"] +'/api/monitors/1.json'
				parameters = {'Monitor[Function]': 'Monitor'}
				url.call(urlConnect, parameters)
			if Level == 30:
				urlConnect = 'http://'+ Parameters["Mode1"] +'/index.php?username='+ Parameters["Username"] +'&password='+ Parameters["Password"] +'&action=login&view=console'
				url.call(urlConnect)
				urlConnect = 'http://'+ Parameters["Mode1"] +'/api/monitors/1.json'
				parameters = {'Monitor[Function]':'Modect'}
				url.call(urlConnect, parameters)
			if Level == 40:
				urlConnect = 'http://'+ Parameters["Mode1"] +'/index.php?username='+ Parameters["Username"] +'&password='+ Parameters["Password"] +'&action=login&view=console'
				url.call(urlConnect)
				urlConnect = 'http://'+ Parameters["Mode1"] +'/api/monitors/1.json'
				parameters = {'Monitor[Function]':'Record'}
				url.call(urlConnect, parameters)
			if Level == 50:
				urlConnect = 'http://'+ Parameters["Mode1"] +'/index.php?username='+ Parameters["Username"] +'&password='+ Parameters["Password"] +'&action=login&view=console'
				url.call(urlConnect)
				urlConnect = 'http://'+ Parameters["Mode1"] +'/api/monitors/1.json'
				parameters = {'Monitor[Function]':'Mocord'}
				url.call(urlConnect, parameters)
			if Level == 60:
				urlConnect = 'http://'+ Parameters["Mode1"] +'/index.php?username='+ Parameters["Username"] +'&password='+ Parameters["Password"] +'&action=login&view=console'
				url.call(urlConnect)
				urlConnect = 'http://'+ Parameters["Mode1"] +'/api/monitors/1.json'
				parameters = {'Monitor[Function]':'Nodect'}
				url.call(urlConnect, parameters)
		
		if Unit == 3:
			if Command == "On":
				urlConnect = 'http://'+ Parameters["Mode1"] +'/index.php?username='+ Parameters["Username"] +'&password='+ Parameters["Password"] +'&action=login&view=console'
				url.call(urlConnect)
				urlConnect = 'http://'+ Parameters["Mode1"] +'/api/monitors/1.json'
				parameters = {'Monitor[Enabled]':'1'}
				url.call(urlConnect, parameters)
			
			if Command == "Off":
				urlConnect = 'http://'+ Parameters["Mode1"] +'/index.php?username='+ Parameters["Username"] +'&password='+ Parameters["Password"] +'&action=login&view=console'
				url.call(urlConnect)
				urlConnect = 'http://'+ Parameters["Mode1"] +'/api/monitors/1.json'
				parameters = {'Monitor[Enabled]':'0'}
				url.call(urlConnect, parameters)
			

	def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
		Domoticz.Log("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)

	def onDisconnect(self, Connection):
		Domoticz.Log("onDisconnect called")

	def onHeartbeat(self):
		Domoticz.Log("onHeartbeat called")

global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)

def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

def onNotification(Data):
    global _plugin
    _plugin.onNotification(Data)

def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

	# Generic helper functions
def DumpConfigToLog():
	for x in Parameters:
		if Parameters[x] != "":
			Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
	Domoticz.Debug("Device count: " + str(len(Devices)))
	for x in Devices:
		Domoticz.Debug("Device:		   " + str(x) + " - " + str(Devices[x]))
		Domoticz.Debug("Device ID:	   '" + str(Devices[x].ID) + "'")
		Domoticz.Debug("Device Name:	 '" + Devices[x].Name + "'")
		Domoticz.Debug("Device nValue:	" + str(Devices[x].nValue))
		Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
		Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
	return
