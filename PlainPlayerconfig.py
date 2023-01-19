import winreg as reg

class Reg():
	def __init__(self):
		pass
		
	def InitKey(self):
		key=reg.CreateKey(reg.HKEY_CURRENT_USER,"PlainPlayer.config")
		reg.SetValueEx(key,"Savelyricfiles",1,reg.REG_SZ,"True")
		reg.SetValueEx(key,"Loopmode",1,reg.REG_SZ,"Singleloop")
		reg.CloseKey(key)
		
	def ReadKey(self,keyname):
		try:
			key=reg.OpenKey(reg.HKEY_CURRENT_USER,"PlainPlayer.config")
			value,t=reg.QueryValueEx(key,keyname)
			reg.CloseKey(key)
			return value
		except:
			return "Error"
	
	def Savelyricfiles(self,bl):
		key=reg.OpenKey(reg.HKEY_CURRENT_USER,"PlainPlayer.config",0,reg.KEY_SET_VALUE)
		reg.SetValueEx(key,"Savelyricfiles",1,reg.REG_SZ,bl)
		reg.CloseKey(key)
	
	def Loopmode(self,md):
		key=reg.OpenKey(reg.HKEY_CURRENT_USER,"PlainPlayer.config",0,reg.KEY_SET_VALUE)
		reg.SetValueEx(key,"Loopmode",1,reg.REG_SZ,md)
		reg.CloseKey(key)

	def Loadskin(self,bl):
		key=reg.OpenKey(reg.HKEY_CURRENT_USER,"PlainPlayer.config",0,reg.KEY_SET_VALUE)
		reg.SetValueEx(key,"Loadskin",1,reg.REG_SZ,bl)
		reg.CloseKey(key)
	
	def Volume(self,size):
		key=reg.OpenKey(reg.HKEY_CURRENT_USER,"PlainPlayer.config",0,reg.KEY_SET_VALUE)
		reg.SetValueEx(key,"Volume",1,reg.REG_QWORD,size)
		reg.CloseKey(key)

	def InspectKey(self):
		try:
			key=reg.OpenKey(reg.HKEY_CURRENT_USER,"PlainPlayer.config",0,reg.KEY_SET_VALUE)
			return "Has Key"
		except:
			return "No Key"