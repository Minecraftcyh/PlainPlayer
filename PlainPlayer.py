#try:
import os,sys,time,zipfile
from Media import *
from PlainPlayerconfig import *
from PlainPlayersetup import *
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

mp=Musicplayer("mp")
lr=Lyric()
cf=Reg()
mf=Musicinfo()

class PlayerGui(QMainWindow):
	def __init__(self):
		super().__init__()
		#self.setFixedSize(self.width(),self.height()) #固定窗口大小
		#self.font=QFont()
		#self.font.setFamily("Microsoft YaHei")
		tf=cf.InspectKey()
		if tf == "No Key":
			cf.InitKey()
		self.GuiPart()

	def GuiPart(self):
		self.resize(250,260) #设置窗口大小
		self.setWindowTitle("PlainPlayer by cyh") #窗口标题
		self.setWindowIcon(QIcon('plainself.ico')) #窗口图标
		self.setAcceptDrops(True)

		self.start_button=QPushButton("开始播放",self)
		self.start_button.clicked.connect(self.start)
		self.start_button.setGeometry(0,75,125,25) #(x坐标，y坐标，宽，高)
		self.start_button.setObjectName("sbtn")

		self.pause_button=QPushButton("暂停播放",self) 
		self.pause_button.clicked.connect(self.pause)
		self.pause_button.setGeometry(125,75,125,25) #(x坐标，y坐标，宽，高)
		self.pause_button.setObjectName("pbtn")

		self.singleloop_radio=QRadioButton("单曲循环",self)
		self.singleloop_radio.setGeometry(0,100,65,25)
		self.singleloop_radio.setObjectName("slr")
		self.listloop_radio=QRadioButton("列表循环",self)
		self.listloop_radio.setGeometry(65,100,65,25)
		self.listloop_radio.setObjectName("llr")

		self.loopmode_group=QButtonGroup(self)
		self.loopmode_group.addButton(self.singleloop_radio,1)
		self.loopmode_group.addButton(self.listloop_radio,2)

		if cf.ReadKey("Loopmode") == "Singleloop":
			self.singleloop_radio.setChecked(True)
		else:
			self.listloop_radio.setChecked(True)			

		self.find_music_button=QPushButton("寻找音频",self) 
		self.find_music_button.clicked.connect(self.openfile)
		self.find_music_button.setGeometry(130,100,60,25) #(x坐标，y坐标，宽，高)
		self.find_music_button.setObjectName("fmbtn")

		self.music_dir_button=QPushButton("音频目录",self)
		self.music_dir_button.clicked.connect(self.addmp3)
		self.music_dir_button.setGeometry(190,100,60,25) #(x坐标，y坐标，宽，高)
		self.music_dir_button.setObjectName("mdbtn")

		self.setUp=Set()
		self.setting_button=QPushButton(QIcon("Set Image.png"),"",self)
		self.setting_button.clicked.connect(self.setUp.show)
		self.setting_button.clicked.connect(lambda:self.start_button.setEnabled(False))
		self.setting_button.clicked.connect(self.setUp.open_event)
		self.setting_button.setGeometry(225,0,25,25)
		self.setting_button.setFlat(True)
		self.setting_button.setObjectName("setbutton")

		self.input_entry=QLineEdit(self) 
		self.input_entry.setGeometry(100,25,150,25) #(x坐标，y坐标，宽，高)

		self.input_music_label=QLabel(self)
		self.input_music_label.setText("输入音频文件:")
		self.input_music_label.setAlignment(Qt.AlignCenter)
		self.input_music_label.setGeometry(0,25,100,25)
		self.input_music_label.setObjectName("iml")

		self.is_playing_label=QLabel(self)
		self.is_playing_label.setText("当前播放:")
		self.is_playing_label.setAlignment(Qt.AlignCenter)
		self.is_playing_label.setGeometry(0,0,100,25)
		self.is_playing_label.setObjectName("ipl")

		self.playing_label=QLabel(self)
		self.playing_label.setText("没有音频在播放")
		self.playing_label.setAlignment(Qt.AlignCenter)
		self.playing_label.setStyleSheet("color:green")
		self.playing_label.setGeometry(100,0,125,25)
		self.playing_label.setObjectName("pl")

		self.display_time_label=QLabel(self) 
		self.display_time_label.setText("00:00")
		self.display_time_label.setAlignment(Qt.AlignCenter)
		self.display_time_label.setGeometry(210,50,40,25)
		self.display_time_label.setObjectName("time")

		self.display_lryic_listwidget_font=QFont()
		self.display_lryic_listwidget_font.setFamily("Microsoft YaHei")
		self.display_lryic_listwidget_font.setPointSize(8)

		self.display_lryic_listwidget=QListWidget(self)
		self.display_lryic_listwidget.setGeometry(0,180,250,80)
		self.display_lryic_listwidget.clear()

		self.music_list_listwidget=QListWidget(self) 
		self.music_list_listwidget.setGeometry(0,125,250,55)
		self.music_list_listwidget.itemDoubleClicked.connect(self.mp3selection)
		self.music_list_listwidget.clear()

		self.display_progressbar=QProgressBar(self)
		self.display_progressbar.setGeometry(0,50,210,12)
		self.display_progressbar.setRange(0,1)
		self.display_progressbar.setValue(0)
		self.display_progressbar.setTextVisible(False)

		self.display_scrollbar=QScrollBar(Qt.Horizontal,self) 
		self.display_scrollbar.setGeometry(0,62,210,13)
		self.display_scrollbar.actionTriggered.connect(self.Probar)
		self.display_scrollbar.setObjectName("ds")

		self.count_timer=QTimer()
		self.count_timer.timeout.connect(self.Pro)

	def closeEvent(self,event):		
		if self.loopmode_group.checkedId() == 1:
			cf.Loopmode("Singleloop")
		else:
			cf.Loopmode("Listloop")

	def dragEnterEvent(self,event):
		self.drop=event.mimeData().text()
		self.music_list_listwidget.addItem(event.mimeData().text().replace("file:///",""))
#
	def commandline_start(self,path):
		self.input_entry.setText(path)
		if os.path.exists(path):
			self.playing_label.setText(os.path.split(path)[1])
			mp.start(self.cm(path))
			mp.setvolume(cf.ReadKey("Volume"))
			self.input_entry.setFocusPolicy(Qt.NoFocus)
			self.lyric()
			sl=mp.duration()
			self.display_scrollbar.setMaximum(sl)
			self.display_progressbar.setRange(0,sl)
			self.Pro()
			
	def commandline_lryic(self,name):
		with open(os.path.basename(name)+".lrc","w",encoding="utf-8") as lf:
				wins=lr.lyric_all(name)
				if wins != "No Internet":
					for i in wins:
						lf.write(i)
						lf.write("\n")
				else:
					print("连接失败")

	def cm(self,path): #转换音频
		if os.path.splitext(path)[1] not in (".mp3",".wav"):
			if os.path.splitext(path)[1] != ".mp":
				if not os.path.exists("C:\\Users\\"+os.getlogin()+"\\AppData\\Local\\Temp\\temp_mp_"+os.path.splitext(os.path.split(path)[1])[0]+".mp3"):
					path=mp.convertformat(path,"C:\\Users\\"+os.getlogin()+"\\AppData\\Local\\Temp\\temp_mp_","mp3")
				else:
					path="C:\\Users\\"+os.getlogin()+"\\AppData\\Local\\Temp\\temp_mp_"+os.path.splitext(os.path.split(path)[1])[0]+".mp3"
			else:
				return "mp"
		return path
					
	def start(self):
		path=self.input_entry.text()
		if os.path.exists(path):
			self.playing_label.setText(os.path.split(path)[1]+" ")
			if self.start_button.text()=="开始播放":
				self.start_button.setText("停止播放")
				new_path=self.cm(path)
				if new_path == "mp":
					mdict=self.Integrated_Music(path)
					mp.start(mdict["mp3"])
					self.lyric()
				else:
					mp.start(new_path)
					self.lyric()
				mp.setvolume(cf.ReadKey("Volume"))
				self.input_entry.setEnabled(False)
				sl=mp.duration()
				self.display_scrollbar.setMaximum(sl)
				self.display_progressbar.setRange(0,sl)
				self.Pro()
			else:
				self.playing_label.setStyleSheet("color:green")
				self.start_button.setText("开始播放")
				self.pause_button.setText("暂停播放")
				self.input_entry.setEnabled(True)
				mp.stop()
				self.display_progressbar.setValue(0)
				self.display_scrollbar.setValue(0)
		else:
			self.playing_label.setText("没有找到文件")
			QMessageBox.critical(self,"错误","没有找到文件")
		
	def pause(self):
		if self.start_button.text() == "开始播放":
			QMessageBox.information(self,"提示","还没有音频在播放")
			return
		if self.pause_button.text() == "暂停播放":
			self.pause_button.setText("恢复播放")
			mp.pause()
		else:
			self.pause_button.setText("暂停播放")
			mp.resume()
		
	def openfile(self): #寻找音频文件
		filepath,filetype=QFileDialog.getOpenFileName(player,"选取音频文件",os.getcwd(),"mp3 (*.mp3);;wav (*.wav);;mp (*.mp);;other (*)")
		if filepath == " " or filepath == "":
			return
		self.input_entry.setText(filepath)
		filename=os.path.basename(filepath)#带后缀的文件名
		self.music_list_listwidget.clear()
		self.music_list_listwidget.addItem(filename)
		self.music_list_listwidget.setCurrentRow(0)
		self.playing_label.setText(os.path.split(self.input_entry.text())[1]+" ")
		if os.path.splitext(filename)[1] == ".mp":
			dc=self.Integrated_Music(filepath)["lrc"]
			self.lyric(dc)
		else:
			self.lyric()
		
	def autolrc(self,sp): #滚动歌词
		sf=self.input_entry.text()
		if os.path.splitext(self.input_entry.text())[-1] not in (".mp3"):
				ans=lr.lyric_all(os.path.splitext(os.path.basename(self.input_entry.text()))[0])
		else:
			if os.path.splitext(sf)[1] != ".mp":
				dinfo=mf.GetInfo(sf)
				info=dinfo["Title"]+" "+dinfo["Artist"]
				ans=lr.lyric_all(info)#os.path.basename(self.input_entry.text()).split('.')[0])
			else:
				ans=self.Integrated_Music(self.input_entry.text())["lrc"]
		if ans == "No Internet":
			self.display_lryic_listwidget.clear()
			self.display_lryic_listwidget.addItem("连接失效")
			return
		musicLrc=""
		for i in ans:
			musicLrc=musicLrc+i+"\n"
		musicDict={}  #用字典来保存该时刻对应的歌词
		musicL=[]
			#对歌词列表进行切割
		musicList=musicLrc.strip().splitlines()
		for i in musicList:
			musicTime=i.split("]")
			for j in musicTime[:-1]:
				musicTime1=j[1:].split(":")
				templ=[]
				for i in musicTime1:
					try:
						float(i)
						templ.append(i)
					except:
						pass
				musicTime1=templ
				print(musicTime1)
				musicTL=float(musicTime1[0])*60+float(musicTime1[1])
				musicDict[musicTL]=musicTime[-1]
		for i in musicDict:
			musicL.append(i)#将时间存到列表中
		musicL.sort()#对时间进行排序
			#按时间顺序循环输出歌词
		for i in range(len(musicL)):
			if i == 0:
				self.display_lryic_listwidget.setCurrentRow(0)
			elif i == 1:
				self.display_lryic_listwidget.setCurrentRow(0)
			else:
				if sp >= musicL[i-1] and sp <= musicL[i]:
					self.display_lryic_listwidget.setCurrentRow(i-1)
					return
		
	def lyric(self,*args): #添加歌词进listwidget
		if len(args) == 1:
			with open(args[0],"r",encoding="utf-8") as olm:
				ins=olm.readlines()		
			self.display_lryic_listwidget.clear()
			self.display_lryic_listwidget.setCurrentRow(0)
			for i in ins:
				n1=i.find("]")+1
				self.display_lryic_listwidget.addItem(i[n1:].replace("\n",""))
		else:
			path=os.getcwd()+os.path.basename(self.input_entry.text())+".lrc"
			if os.path.isfile(path):
				with open(path,"r",encoding="utf-8") as hf:
					ins=hf.read()
				for i in ins:
					self.display_lryic_listwidget.addItem(i)
				return
			if os.path.splitext(self.input_entry.text())[-1] not in (".mp3"):
				ins=lr.lyric_text(os.path.splitext(os.path.basename(self.input_entry.text()))[0])
			else:
				dinfo=mf.GetInfo(self.input_entry.text())
				info=dinfo["Title"]+" "+dinfo["Artist"]
				ins=lr.lyric_text(info)
			if ins == "No Internet":
				self.display_lryic_listwidget.clear()
				self.display_lryic_listwidget.addItem("连接失效")
				return
			rk=cf.ReadKey("Savelyricfiles")
			if rk == "True":
				with open(os.path.basename(self.input_entry.text())+".lrc","w",encoding="utf-8") as lf:
					wins=lr.lyric_all(info)
					if wins != "No Internet":
						for i in wins:
							lf.write(i)
							lf.write("\n")
			if ins == 0:
				QMessageBox.information(player,"找不到歌词","可能是歌曲作者或名字不正确")
				return
			self.display_lryic_listwidget.clear()
			self.display_lryic_listwidget.setCurrentRow(0)
			if ins == "No Lyric":
				self.display_lryic_listwidget.addItem("\n 暂无歌词")
				return
			for i in ins:
				self.display_lryic_listwidget.addItem(i)
			
	def Probar(self,action):
		if self.start_button.text() == "开始播放":
			self.display_scrollbar.setValue(0)
			return
		pos=self.display_scrollbar.value()
		mp.jump(int(pos))
		
	def Pro(self):
		sl=mp.duration()  #音频长度
		if sl == 0:
			return
		sp=mp.position()  #播放到的位置
		self.tfm(sp/1000)#把秒换算成分钟格式:01：00
		self.autolrc(sp/1000)
		self.scroll_label()
		self.display_progressbar.setValue(sp) #播放到的位置
		self.display_scrollbar.setValue(sp)
		if sp < sl:
			self.count_timer.start(100)
		else:
			if cf.ReadKey("Loopmode") == "Singleloop":
				self.start()
			else:
				pos=self.music_list_listwidget.selectedIndexes()[0].row()
				self.music_list_listwidget.setCurrentRow(pos+1)
				posid=self.music_list_listwidget.selectedItems()[0].text()
				pid=os.path.basename(posid)
				self.playing_label.setText(pid)
				self.input_entry.setText(posid)
				self.start_button.setText("开始播放")
				mp.stop()
				self.start()

	def addmp3(self):
		path=QFileDialog.getExistingDirectory(player)  # 获得选择好的文件夹
		path=path.replace("/","\\")
		if path != "":
			self.music_list_listwidget.clear()
			for root,dirs,files in os.walk(path):
				for file in os.listdir(root):  # 不仅仅是文件，当前目录下的文件夹也会被认为遍历到
					lits=os.path.splitext(file)
					suffix=lits[-1]
					if suffix.lower() in (".mp3",".wav",".aac",".ogg",".flac",".m4a") and os.path.isfile(os.path.join(root,file)):
						np=os.path.join(root,file)
						self.music_list_listwidget.addItem(np)
		
	def mp3selection(self):
		filepath=self.music_list_listwidget.selectedItems()[0].text()
		filename=os.path.basename(filepath)
		self.playing_label.setText(filename+" ")
		self.input_entry.setText(filepath)
		self.start_button.setText("开始播放")
		mp.stop()
		self.start()
		
	def tfm(self,sp):
		time_st=int(sp)
		if time_st > 59:
			time_nd=time_st%60
			time_rd=time_st//60
			if time_nd < 59 and len(str(time_nd)) != 2:
				self.display_time_label.setText("0"+str(time_rd)+":0"+str(time_nd))
			else:
				self.display_time_label.setText("0"+str(time_rd)+":"+str(time_nd))
		else:
			if len(str(time_st)) == 1:
				self.display_time_label.setText("00:0"+str(time_st))
			else:
				self.display_time_label.setText("00:"+str(time_st))
				
	def scroll_label(self):
		self.playing_label.setStyleSheet("color:blue")
		nr=self.playing_label.text()
		if len(nr) > 21:			  
			new_nr=nr[1:]+nr[0]
			nr=new_nr
			self.playing_label.setText(nr)
		
	def Integrated_Music(self,path):
		md={}
		zf=zipfile.ZipFile(path,"r")
		for fn in zf.namelist():
			zf.extract(fn,"C:\\Users\\"+os.getlogin()+"\\AppData\\Local\\Temp\\")
			if os.path.splitext(fn)[1] == ".mp3":
				md["mp3"]="C:\\Users\\"+os.getlogin()+"\\AppData\\Local\\Temp\\"+fn
			elif os.path.splitext(fn)[1] == ".lrc":
				md["lrc"]="C:\\Users\\"+os.getlogin()+"\\AppData\\Local\\Temp\\"+fn
		return md	

class Set(QWidget,Setup):
	def __init__(self):
		super().__init__()
		self.setGui(self,mp,cf)

	def open_event(self):
		self.volume_scrollbar.setValue(cf.ReadKey("Volume"))
		nr=cf.ReadKey("Savelyricfiles")
		if nr == "True":
			self.save_lyricfile_radio.setChecked(True)
		elif nr == "False":
			self.unsave_lyricfile_radio.setChecked(True)
		else:
			cf.InitKey()
			self.save_lyricfile_radio.setChecked(True)

	def closeEvent(self,event):
		if self.is_lyricfile_group.checkedId() == 1:
			cf.Savelyricfiles("True")
		else:
			cf.Savelyricfiles("False")
		player.start_button.setEnabled(True)

	def changevolume(self,action):
		self.volume_scrollbar.setToolTip(str(self.volume_scrollbar.value()))
		self.volume_label.setText("当前音量: "+str(cf.ReadKey("Volume")))
		size=self.volume_scrollbar.value()
		mp.setvolume(size)
		cf.Volume(size)

class Other:
	def __init__(self):
		pass

	@staticmethod
	def LoadQss(self):
		try:
			with open("PlainPlayerStyle.qss","r",encoding="utf-8") as qs:
				return qs.read()
		except:
			return 0

	@staticmethod
	def Launcher(self):
		from getopt import getopt
		style=Other.LoadQss("self")
		opti,args=getopt(sys.argv[1:],"-h-n-l:-s:",["help","nostyle","lryic=","start="])
		for optn,optv in opti:
			print(optn,optv)
			if optn in ("-n","--nosytle") or cf.ReadKey("Loadskin") == "False":
				window.setStyleSheet('*{font-family:"Microsoft YaHei";}\nQRadioButton#slr,QRadioButton#llr{spacing:2px;}\nQPushButton#csbtn{border-radius:0px;\nbackground-color:white}')
			else:window.setStyleSheet(style)
			if optn in ("-l","--lryic"):
				player.commandline_lryic(optv.replace(":","",1))
			elif optn in ("-s","--start"):
				player.commandline_start(optv)                        # 显示窗体
				player.show()
				sys.exit(window.exec_())
		else:
			if cf.ReadKey("Loadskin") == "False":
				window.setStyleSheet('*{font-family:"Microsoft YaHei";}\nQRadioButton#slr,QRadioButton#llr{spacing:2px;}\nQPushButton#csbtn{border-radius:0px;\nbackground-color:white}')
			else:window.setStyleSheet(style)
			player.show()
			sys.exit(window.exec_())

if __name__ == "__main__":
	window=QApplication(sys.argv)
	player=PlayerGui()
	Other().Launcher("other")