from PlainPlayerconfig import *
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Setup(object):
		def __init__(self):
			pass

		def setGui(self,window,mp,cf):
			self.resize(200,100) #设置窗口大小
			self.setWindowTitle("PlainPlayer's setting") #窗口标题
			self.setWindowIcon(QIcon('plainplayer.ico')) #窗口图标
			self.setFixedSize(self.width(),self.height()) #固定窗口大小

			self.savelyricfile_label=QLabel("是否保存歌词:",self)
			self.savelyricfile_label.setGeometry(0,0,80,25) #(x坐标，y坐标，宽，高)

			self.save_lyricfile_radio=QRadioButton("保存",self)
			self.save_lyricfile_radio.setGeometry(90,0,50,25) #(x坐标，y坐标，宽，高)
			self.save_lyricfile_radio.setObjectName("slrd")
			self.unsave_lyricfile_radio=QRadioButton("不保存",self)
			self.unsave_lyricfile_radio.setGeometry(140,0,60,25) #(x坐标，y坐标，宽，高)
			self.unsave_lyricfile_radio.setObjectName("uslrd")

			self.is_lyricfile_group=QButtonGroup(self)
			self.is_lyricfile_group.addButton(self.save_lyricfile_radio,1)
			self.is_lyricfile_group.addButton(self.unsave_lyricfile_radio,2)

			self.volume_label=QLabel("当前音量: "+str(cf.ReadKey("Volume")),self)
			self.volume_label.setGeometry(0,25,80,25)

			self.volume_scrollbar=QScrollBar(Qt.Horizontal,self) 
			self.volume_scrollbar.setGeometry(80,25,120,25)
			self.volume_scrollbar.actionTriggered.connect(self.changevolume)
			self.volume_scrollbar.setMaximum(100)
			self.volume_scrollbar.setToolTip(str(cf.ReadKey("Volume")))
			self.volume_scrollbar.setObjectName("vs")

			self.close_save_button=QPushButton("保存配置",self)
			self.close_save_button.clicked.connect(self.close)
			self.close_save_button.setGeometry(0,75,200,25) #(x坐标，y坐标，宽，高)
			self.close_save_button.setObjectName("csbtn")