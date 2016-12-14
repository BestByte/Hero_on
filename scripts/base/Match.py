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

class Match(KBEngine.Base, GameObject):
	"""
	这是一个匹配系统
	当客户端登录时，PVP模式下，发出PVP请求，
	匹配系统格局两者的champion得分相近时匹配创建space
	KBEngine的space是一个抽象空间的概念，一个空间可以被脚本层视为游戏场景、游戏房间、甚至是一个宇宙。
	"""
	def __init__(self):
		KBEngine.Base.__init__(self)
		GameObject.__init__(self)

	
		#match1 建立的决定确认的各个实体
		self.playerCal={}
		#self.players={}
		
	

		# 将自己注册到共享数据中， 在当前进程KBEngine.globalData["Halls"]返回的是Halls实体，其他进程中
		# 由于实体不在那个进程所以KBEngine.globalData["Halls"]返回的是mailbox
		# 因此调用KBEngine.globalData["Halls"].xxx方法必须在def定义，允许远程访问

		# 向全局共享数据中注册这个管理器的mailbox以便在所有逻辑进程中可以方便的访问
		KBEngine.globalData["match%i"%int(os.getenv("KBE_BOOTIDX_GROUP"))] = self
		DEBUG_MSG("KBEngine.globalData[match%i)"%int(os.getenv("KBE_BOOTIDX_GROUP")))

		# 通过添加一个定时器延时执行房间的创建，确保一些状态在此期间能够初始化完毕
		#self.addTimer(3, 1, 1)

	

	def eachPVPMatch(self,player,player_match_number):
		"""
		player:MailBox
		player_match_num:Match所在的baseAPP编号
		""" 
		charge_value=200 #起始设定的与玩家奖杯的差值
		charge_id=1 #记录玩家的标号
		for x in self.playerMactch.values():
			
				#若是在线的正要匹配的玩家当中，与匹配的玩家的奖杯数差值最少的玩家
				#则要传给baseapp1的匹配实体Match
				#x属于本线程的实体，直接访问champion属性
			if charge_value<abs(x.champion-self.reqGetAttrs(player)) and x.id != player.id:#在同一线程中，不能让两者重复
					charge_value=abs(x.champion-self.reqGetAttrs(player))
					charge_id=x.id #记录最小差值玩家的标号
			else:
				charge_value=abs(x.champion-self.reqGetAttrs(player))
				charge_id=x.id
		if KBEngine.entities.has_key(charge_id):
			matchedPlayer=KBEngine.entities[charge_id]
		else:
			matchedPlayer=None

			#主match排序
		KBEngine.globalData["Master"].addPVPResult(matchedPlayer,matchedPlayer.champion,plalyer,self.reqGetAttrs(player),player_match_number,int(os.getenv("KBE_BOOTIDX_GROUP")))

		DEBUG_MSG("KBEngine.globalData['match1'].addPVPResult(matchedPlayer[%s],matchedPlayer.champion[%i],plalyer[%s],self.reqGetAttrs(player,champion)[%i]),os.getenv('KBE_BOOTIDX_GROUP')[%i]" % (matchedPlayer,matchedPlayer.champion,plalyer,self.reqGetAttrs(player),int(os.getenv("KBE_BOOTIDX_GROUP"))))

	def reqGetAttrs(self, mailbox):
		mailbox.onGetAttr(self.champion)
		DEBUG_MSG("Player[%i].reqGetAttr(self, mailbox,attrs [%s]):" % (mailbox.id))

	#-----------------------------------------------------------
	#                              Callbacks
	#-----------------------------------------------------------
	def onTimer(self, tid, userArg):
		"""
		KBEngine method.
		引擎回调timer触发
		"""
		#DEBUG_MSG("%s::onTimer: %i, tid:%i, arg:%i" % (self.getScriptName(), self.id, tid, userArg))
		
		GameObject.onTimer(self, tid, userArg)

	

