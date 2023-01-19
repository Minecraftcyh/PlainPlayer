from ctypes import c_buffer, windll
from ctypes import cast, POINTER
from pydub import AudioSegment
from sys import getfilesystemencoding
import requests,os,json,base64,re,time
from scrapy.selector import Selector
from binascii import hexlify
from Crypto.Cipher import AES

class Musicplayer:
	def __init__(self,classname): #初始化
		self.name=classname
		self.buf=c_buffer(255)
	
	def start(self,path): #播放和停止
		windll.winmm.mciSendStringW('open "'+path+'" type mpegvideo alias '+self.name,self.buf,254,0)
		windll.winmm.mciSendStringW("play "+self.name+" from 0",self.buf,254,0)
	
	def stop(self):
		windll.winmm.mciSendStringW("close "+self.name,self.buf,254,0)
		
	def pause(self): #暂停和回恢复
		windll.winmm.mciSendStringW("pause "+self.name,self.buf,254,0)
		
	def resume(self):
		windll.winmm.mciSendStringW("resume "+self.name,self.buf,254,0)
		
	def duration(self):
		command="status "+self.name+" length"
		ec=getfilesystemencoding()
		command=command.encode(ec)
		windll.winmm.mciSendStringA(command,self.buf,254,0)
		times=self.buf.value.decode()
		if times == " " or times == "":
			times=0
		return int(times)
		
	def position(self): #获取音频时长和播放进度
		command="status "+self.name+" position"
		ec=getfilesystemencoding()
		command=command.encode(ec)
		windll.winmm.mciSendStringA(command,self.buf,254,0)
		times=self.buf.value.decode()
		if times == " " or times == "":
			times=0
		return int(times)
		
	def jump(self,jumptime): #跳转到时间
		windll.winmm.mciSendStringW("play "+self.name+" from "+str(jumptime),self.buf, 254, 0)

	def convertformat(self,filepath,outputpath,fom):
		print(filepath)
		song=AudioSegment.from_file(filepath)
		path=outputpath+os.path.splitext(os.path.split(filepath)[1])[0]+".mp3"
		song.export(path,format=fom)
		return path
		
	def getvolume(self):
		command="status "+self.name+" volume"
		ec=getfilesystemencoding()
		command=command.encode(ec)
		windll.winmm.mciSendStringA(command,self.buf,254,0)
		if self.buf.value.decode() == "":
			volume="0"
		else:
			volume=str(int(self.buf.value.decode())//10)
		return volume
		
	def setvolume(self,size):
		command="setaudio "+self.name+" volume to "+str(int(size)*10)
		ec=getfilesystemencoding()
		command=command.encode(ec)
		windll.winmm.mciSendStringA(command,self.buf,254,0)
		volume=self.buf.value.decode()
		
class Musicinfo:
	def __init__(self):
		pass
	
	def GetInfo(self,path):
		InfoDictionary={}
		OutPut=os.popen(r'eyeD3 "'+path+'"')
		ReadOutPut=OutPut.read()
		Result=self.CutOutPut(ReadOutPut)
		TitlePosition,ArtistPosition,Title,Artist=self.GetPostition(Result)
		DictionaryTitle=Title[TitlePosition+2:]
		DictionaryArtist=Artist[ArtistPosition+2:]
		InfoDictionary["Title"]=DictionaryTitle
		InfoDictionary["Artist"]=DictionaryArtist
		return InfoDictionary
	
	def CutOutPut(self,output):
		HeadPosition=output.find("title")
		EndPosition=output.find("album")
		PositionResult=output[HeadPosition:EndPosition]
		ReplaceResult=PositionResult.replace("\n","&")
		return ReplaceResult

	def GetPostition(self,cutresult):
		SeparatePosition=cutresult.find("&")
		Title=cutresult[:SeparatePosition]
		GetTitlePosition=Title.find(":")
		Artist=cutresult[SeparatePosition:-1]
		GetArtistPosition=Artist.find(":")
		return GetTitlePosition,GetArtistPosition,Title,Artist

class Videoplayer():
	def __init__(self):
		pass
	
	def video(self,vp,autoexit=True,showmode=0,ixy=None,ss=0):
		command="ffplay -showmode "+str(showmode)+" -ss "+str(ss)
		xy=""
		if autoexit:
			command+=" -autoexit "
		if ixy != None:
			xy+=" -x "+str(ixy[0])
		if ixy != None:
			xy+=" -y "+str(ixy[1])
		command+=' -i "'+vp+'"'
		print(command+"\n")
		rcode=os.popen(command)
		return rcode.read()
		
class Encrypyed():
	def __init__(self):
		self.pub_key = '010001'
		self.modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
		self.nonce ='0CoJUm6Qyw8W8jud'

	def create_secret_key(self, size):
		return hexlify(os.urandom(size))[:16].decode('utf-8')

	def aes_encrypt(self,text, key):
		iv="0102030405060708"
		pad=16-len(text) % 16
		text=text + pad * chr(pad)
		encryptor = AES.new(key.encode('utf-8'),AES.MODE_CBC,iv.encode('utf-8'))
		result = encryptor.encrypt(text.encode('utf-8'))
		result_str = base64.b64encode(result).decode('utf-8')
		return result_str

	def rsa_encrpt(self,text, pubKey, modulus):
		text = text[::-1]
		rs = pow(int(hexlify(text.encode('utf-8')), 16), int(pubKey, 16), int(modulus, 16))
		return format(rs, 'x').zfill(256)

	def work(self,ids,br=128000):
		text = {'ids': [ids], 'br': br, 'csrf_token': ''}
		text = json.dumps(text)
		i=self.create_secret_key(16)
		encText =self.aes_encrypt(text, self.nonce)
		encText=self.aes_encrypt(encText,i)
		encSecKey=self.rsa_encrpt(i,self.pub_key,self.modulus)
		data = {'params': encText, 'encSecKey': encSecKey}
		return data

	def search(self,text):
		text = json.dumps(text)
		i = self.create_secret_key(16)
		encText = self.aes_encrypt(text, self.nonce)
		encText = self.aes_encrypt(encText, i)
		encSecKey = self.rsa_encrpt(i, self.pub_key, self.modulus)
		data = {'params': encText, 'encSecKey': encSecKey}
		return data
				
class Lyric():
	def __init__(self):
		self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.46',
            'Host': 'music.163.com',
            'Referer': 'http://music.163.com/search/'} ###!!注意，搜索跟歌单的不同之处！！
		self.main_url='http://music.163.com/'
		self.session = requests.Session()
		self.session.headers=self.headers
		self.ep=Encrypyed()
		
	def lyric_text(self,sn):
		ids=self.search_song(sn)
		if ids == "Error":
			return "No Internet"
		url="http://music.163.com/api/song/lyric?"+"id="+str(ids)+"&lv=1&kv=1&tv=-1"
		if ids == 0:
			return 0
		lrc=re.sub(re.compile(r'\[.*\]'),"",json.loads(requests.get(url).text)['lrc']['lyric']).replace("\n","&")		
		lrtemp=""
		lrt=[]
		for i in lrc:
			if i != "&":
				lrtemp=lrtemp+i
			else:
				lrt.append(lrtemp)
				lrtemp=""
		tl=[]
		for i in lrt:
			pa=i.find("[")
			pb=i.find("]")+1
			if i[pa:pb] != i:
				tl.append(i)
		lrt=tl
		if lrt == []:
			return "No Lyric"
		return lrt
		
	def lyric_time(self,sn):
		ids=self.search_song(sn)
		if ids == "Error":
			return "No Internet"
		url="http://music.163.com/api/song/lyric?"+"id="+str(ids)+"&lv=1&kv=1&tv=-1"
		if ids == 0:
			return 0
		lrc=json.loads(requests.get(url).text)['lrc']['lyric'].replace("\n","&")
		lrtemp=""
		lrt=[]
		for i in lrc:
			if i != "&":
				lrtemp=lrtemp+i
			else:
				lrt.append(lrtemp)
				lrtemp=""
		tl=[]
		for i in lrt:
			pa=i.find("[")
			pb=i.find("]")+1
			tl.append(i[pa:pb])
		lrt=tl
		if lrt == []:
			return "No Lyric"
		return lrt
		
	def lyric_all(self,sn):
		ids=self.search_song(sn)
		if ids == "Error":
			return "No Internet"
		url="http://music.163.com/api/song/lyric?"+"id="+str(ids)+"&lv=1&kv=1&tv=-1"
		if ids == 0:
			return 0
		lrc=json.loads(requests.get(url).text)['lrc']['lyric'].replace("\n","&")
		lrtemp=""
		lrt=[]
		for i in lrc:
			if i != "&":
				lrtemp=lrtemp+i
			else:
				lrt.append(lrtemp)
				lrtemp=""
		tl=[]
		for i in lrt:
			pa=i.find("[")
			pb=i.find("]")+1
			if i[pa:pb] != i:
				tl.append(i)
		lrt=tl
		if lrt == []:
			return "No Lyric"
		return lrt

	def search_song(self,search_content,search_type=1,limit=9):
		url = 'http://music.163.com/weapi/cloudsearch/get/web?csrf_token='
		text = {'s': search_content, 'type': search_type, 'offset': 0, 'sub': 'false', 'limit': limit}
		try:
			data = self.ep.search(text)
			resp = self.session.post(url,data=data)
			result = resp.json()
			if result['result']['songCount']<= 0:
				return 0
			else:
				songs = result['result']['songs']
				song=songs[0]
				#for song in songs:
				song_id=song['id']
				"""
				for song in songs:
					song_id,song_name,singer,alia = song['id'],song['name'],song['ar'][0]['name'],song['al']['name']
					print("id:",song_id,"name:",song_name,"singer:",singer,"alia:",alia)
				"""
				return song_id
		except:
			return "Error"
			