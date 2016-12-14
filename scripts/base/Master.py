# -*- coding: utf-8 -*-
import KBEngine
import Functor
import d_spaces
import SCDefine
import Watcher
from KBEDebug import *

from interfaces.GameObject import GameObject
import math
import time
import os

class Master(KBEngine.Base, GameObject):
	"""
	这是一个匹配系统
	当客户端登录时，PVP模式下，发出PVP请求，
	匹配系统格局两者的champion得分相近时匹配创建space
	KBEngine的space是一个抽象空间的概念，一个空间可以被脚本层视为游戏场景、游戏房间、甚至是一个宇宙。
	"""
	def __init__(self):
		KBEngine.Base.__init__(self)
		GameObject.__init__(self)

		#需要匹配的玩家集合
		self.playerMactch={}
		#所有的请求PVP对战的玩家集合

		#Master建立的决定确认的各个实体
		self.playerCal={}
	
		# 将自己注册到共享数据中， 在当前进程KBEngine.globalData["Halls"]返回的是Halls实体，其他进程中
		# 由于实体不在那个进程所以KBEngine.globalData["Halls"]返回的是mailbox
		# 因此调用KBEngine.globalData["Halls"].xxx方法必须在def定义，允许远程访问

		# 向全局共享数据中注册这个管理器的mailbox以便在所有逻辑进程中可以方便的访问
		KBEngine.globalData["Master"] = self
		DEBUG_MSG("KBEngine.globalData[Master]")

	def addPVPMatch(self,player,player_match_num):
		"""
		defined method.

		player:MailBox
		player_match_num:Match所在的baseAPP编号

		目前系统共涉及baseapp5个，其中1、2专门负责match匹配实体，3负责rooms创建房间实体，3、4、5生成player实体、room房间实体
		""" 
		DEBUG_MSG("Match[%i].addPVPMatch" % int(os.getenv("KBE_BOOTIDX_GROUP")))
		
		#在Master上建立，各个match汇总的匹配数据
		self.playerMactch[player.id]=player

		#在Master上建立，各个match汇总的匹配数据
		self.playerCal[player.id]={}

		for x in range(4):
			KBEngine.globalData["match%i"% (x+2)].eachPVPMatch(player,player_match_num)


	def addPVPResult(self,matchedPlayer,matchedChampion, player,playerChampion,player_match_number,match_order):#match_order 是match的启动值

		#主match实体汇总处理
		#考虑到baseapp的顺序match_order
		self.playerCal[player.id][match_order]=matchedPlayer

		#若是所有的match系统都已经传过来匹配值，则进行最终挑选
		if self.playerCal[player.id].__len__()==4:
			cal_result(player_match_number)

	#最终的匹配函数	
	def cal_result(self,player_match_number):
		end_palyer=None
		
		min_val=30
		match_num=0 #最小的玩家所在的baseapp
		for k ,v in self.playerCal[player.id].items():
			if v !=None:
				if min_val>abs(self.reqGetAttrs(v)-self.reqGetAttrs(player)):
					min_val=abs(self.reqGetAttrs(v)-self.reqGetAttrs(player))
					end_palyer=v
					match_num=k

		#下面是根据选出来的两个实体，创建房间
		KBEngine.globalData["Rooms"].createSpace(0,{},self.playerCal[player.id][k], player)

		#选出来两者之后，把它的字典删除了。
		#有个问题，会不会删除太早了？

		del self.playerCal[player.id]
		del KBEngine.globalData["match%i"%player_match_number].playerMatch[player.id]
		del KBEngine.globalData["Master"%k].playerMatch[end_palyer.id]

		#roomID=int(time.time()*100)

		#self.reqEnterRoom(self, roomID,self.playerMactch[player][x], player)
	#---------------------------------------------------------------------
	#                              Callbacks
	#---------------------------------------------------------------------
	def onTimer(self, tid, userArg):
		"""
		KBEngine method.
		???????÷timer??·?
		"""
		#DEBUG_MSG("%s::onTimer: %i, tid:%i, arg:%i" % (self.getScriptName(), self.id, tid, userArg))
		
		GameObject.onTimer(self, tid, userArg)

	

