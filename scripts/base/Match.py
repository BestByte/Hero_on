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
	"""
	def __init__(self):
		KBEngine.Base.__init__(self)
		GameObject.__init__(self)

		#需要匹配的玩家集合
		self.playerMactch={}
		#所有的请求PVP对战的玩家集合

		# 向全局共享数据中注册这个管理器的mailbox以便在所有逻辑进程中可以方便的访问
		KBEngine.globalData["match%i"%int(os.getenv("KBE_BOOTIDX_GROUP"))] = self
		DEBUG_MSG("KBEngine.globalData[match%i)"%int(os.getenv("KBE_BOOTIDX_GROUP")))

	def eachPVPMatch(self,player):
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

			#改为单个baseapp后更改的，若多个baseapp之后，直接删除下面，把下面的注释的重新取消注释即可
			"""
			if charge_value<abs(x.champion-self.reqGetAttrs(player)) and x.id != player.id:#在同一线程中，不能让两者重复
					charge_value=abs(x.champion-self.reqGetAttrs(player))
					charge_id=x.id #记录最小差值玩家的标号
			else:
				charge_value=abs(x.champion-self.reqGetAttrs(player))
				charge_id=x.id
			"""
			if charge_value<abs(x.champion-player.champion) and x.id != player.id:#在同一线程中，不能让两者重复
					charge_value=abs(x.champion-player.champion)
					charge_id=x.id #记录最小差值玩家的标号
			else:
				charge_value=abs(x.champion-player.champion)
				charge_id=x.id
		if KBEngine.entities.has_key(charge_id):
			matchedPlayer=KBEngine.entities[charge_id]
		else:
			matchedPlayer=None

			#主match排序
		KBEngine.globalData["Master"].addPVPResult(matchedPlayer,matchedPlayer.champion,player,player.champion,int(os.getenv("KBE_BOOTIDX_GROUP")))

		DEBUG_MSG("KBEngine.globalData['match1'].addPVPResult(matchedPlayer[%s],matchedPlayer.champion[%i],plalyer[%s],self.reqGetAttrs(player,champion)[%i]),os.getenv('KBE_BOOTIDX_GROUP')[%i]" % (matchedPlayer,matchedPlayer.champion,player,player.champion,int(os.getenv("KBE_BOOTIDX_GROUP"))))

	#多个baseAPP需要
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

	

