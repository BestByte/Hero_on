# -*- coding: utf-8 -*-
import KBEngine
import Functor
import d_spaces
import SCDefine
import Watcher
from KBEDebug import *
from SpaceAlloc import *
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

		#需要匹配的玩家集合
		self.playerMactch={}
		#所有的请求PVP对战的玩家集合

		#match1 建立的决定确认的各个实体
		self.playerCal={}
		#self.players={}
		self.aGroup={}#0到200分
		self.bGroup={}#200到400
		self.cGroup={}
		self.dGroup={}
		self.eGroup={}

		#按照奖牌得分的差异，把不同等级的玩家的键值做一个列表，存储玩家的mailbox
		self.aList=list(self.aGroup.keys())
		self.bList=list(self.bGroup.keys())
		self.cList=list(self.cGroup.keys())
		self.dList=list(self.dGroup.keys())
		self.eList=list(self.eGroup.keys())
		#考虑添加属性
		
		# 初始化空间分配器
		#self.initAlloc()

		# 初始化房间分配器
		self.initRoomAlloc()

		# 将自己注册到共享数据中， 在当前进程KBEngine.globalData["Halls"]返回的是Halls实体，其他进程中
		# 由于实体不在那个进程所以KBEngine.globalData["Halls"]返回的是mailbox
		# 因此调用KBEngine.globalData["Halls"].xxx方法必须在def定义，允许远程访问

		# 向全局共享数据中注册这个管理器的mailbox以便在所有逻辑进程中可以方便的访问
		KBEngine.globalData["match%i"%(os.getenv("KBE_BOOTIDX_GROUP"))] = self

		# 通过添加一个定时器延时执行房间的创建，确保一些状态在此期间能够初始化完毕
		self.addTimer(3, 1, 1)

	def addPVPMatch(self,player,palyer_match_num):
		DEBUG_MSG("Match[%i].addPVPMatch" % (player.id))
		
		#只要是匹配的玩家那么，就建立初始化列表 
		self.playerMactch[player.id]=player

		#在match1上建立，各个match汇总的匹配数据
		KBEngine.globalData["match1"].playerCal[player.id]={}

		for x in range(ser_number-1):
		    KBEngine.globalData["match%i"%(x+1)].eachPVPMatch(player,palyer_match_num)

		#self.charge_value=100#起始设定的与玩家奖杯的差值

	def eachPVPMatch(self,player,player_match_number):
		#player is mailbox
		charge_value=200 #起始设定的与玩家奖杯的差值
		charge_id=1 #记录玩家的标号
		for x in self.playerMactch.values():
			#若是玩家正在匹配中，则状态码为2

		    #if x.state==2:
				#若是在线的正要匹配的玩家当中，与匹配的玩家的奖杯数差值最少的玩家
				#则要传给baseapp1的匹配实体Match
				#x属于本线程的实体，直接访问champion属性
			if charge_value<abs(x.champion-self.reqGetAttrs(player,champion)) and x.id != player.id:#在同一线程中，不能让两者重复
					charge_value=abs(x.champion-self.reqGetAttrs(player,champion))
					charge_id=x.id #记录最小差值玩家的标号
			else:
				charge_value=abs(x.champion-self.reqGetAttrs(player,champion))
				charge_id=x.id
		if KBEngine.entities.has_key(charge_id):
			matchedPlayer=KBEngine.entities[charge_id]
		else:
			matchedPlayer=None

			#主match排序
		KBEngine.globalData["match1"].addPVPResult(matchedPlayer,matchedPlayer.champion,plalyer,self.reqGetAttrs(player,champion),player_match_number,os.getenv("KBE_BOOTIDX_GROUP"))

		DEBUG_MSG("KBEngine.globalData['match1'].addPVPResult(matchedPlayer[%s],matchedPlayer.champion[%i],plalyer[%s],self.reqGetAttrs(player,champion)[%i]),os.getenv('KBE_BOOTIDX_GROUP')[%i]" % (matchedPlayer,matchedPlayer.champion,plalyer,self.reqGetAttrs(player,champion),os.getenv("KBE_BOOTIDX_GROUP")))

	def reqGetAttr(self, mailbox,attrs):
		mailbox.onGetAttr(self.attrs)
		DEBUG_MSG("Player[%i].reqGetAttr(self, mailbox,attrs [%s]):" % (mailbox.id,attrs))

	def addPVPResult(self,matchedPlayer,matchedChampion, player,playerChampion,player_match_number,match_order):#match_order 是match的启动值

		
		#主match实体汇总处理
		#考虑到baseapp的顺序match_order
		self.playerCal[player.id][match_order]=matchedPlayer


		#若是所有的match系统都已经传过来匹配值，则进行最终挑选
		if self.playerCal[player.id].__len__()==ser_number:
			cal_result(player_match_number)

	#最终的匹配函数	
	def cal_result(self,player_match_number):
		end_palyer=None
		
		min_val=30
		match_num=0 #最小的玩家所在的baseapp
		for k ,v in self.playerCal[player.id].items():
			if v !=None:
				if min_val>abs(self.reqGetAttr(v,champion)-self.reqGetAttrs(player,champion)):
					min_val=abs(self.reqGetAttr(v,champion)-self.reqGetAttrs(player,champion))
					end_palyer=v
					match_num=k


		#下面是根据选出来的两个实体，创建房间
		KBEngine.globalData["Romes"].createSpace(0,{},self.playerCal[player.id][k], player)

		#选出来两者之后，把它的字典删除了。
		#有个问题，会不会删除太早了？

		del self.playerCal[player.id]
		del KBEngine.globalData["match%i"%player_match_number].playerMatch[player.id]
		del KBEngine.globalData["match%i"%k].playerMatch[end_palyer.id]

		#roomID=int(time.time()*100)

		#self.reqEnterRoom(self, roomID,self.playerMactch[player][x], player)

	def reqEnterRoom(self,matched_palyer, player):
		"""
		defined.
		客户端调用该接口请求进入房间/桌子
		"""
		DEBUG_MSG("Room.reqEnterRoom: %s" % (self.roomID))
		self.players[player.id] = player

	def onTimer(self, id, userArg):
		"""
		KBEngine method.
		使用addTimer后， 当时间到达则该接口被调用
		@param id		: addTimer 的返回值ID
		@param userArg	: addTimer 最后一个参数所给入的数据
		"""
		DEBUG_MSG(id, userArg)

		if userArg == 1:
			self.createPVPRoom()

	def initRoomAlloc(self):
		# 注册一个定时器，在这个定时器中我们每个周期都创建出一些场景，直到创建完所有
		self._roomAllocs = {}

		self._roomAllocs[0] = RoomAlloc(0)

	def createPVPRoom(self):
		"""
		defined.
		每一秒通过playerLog里的得分一致的玩家来创建房间
		"""
		DEBUG_MSG("Halls[%i].reqEnterRoom: %s" % (self.id, roomID))
		#还需要加点条件
		if len(self.aList)>=2:
			for x in range(len(self.aList)):
				if x%2==0:
					self._roomAllocs[0].createSpace(0,{},self.aList[x],self.aList[x+1])

	def getSpaceAllocs(self):
		return self._roomAllocs
		
	
	def loginToSpace(self, avatarEntity, spaceUType, context):
		"""
		defined method.
		某个玩家请求登陆到某个space中
		"""
		self._roomAllocs[spaceUType].loginToSpace(avatarEntity, context)
	
	def logoutSpace(self, avatarID, spaceKey):
		"""
		defined method.
		某个玩家请求登出这个space
		"""
		for spaceAlloc in self._roomAllocs.values():
			space = spaceAlloc.getSpaces().get(spaceKey)
			if space:
				space.logoutSpace(avatarID)
				
	def teleportSpace(self, entityMailbox, spaceUType, position, direction, context):
		"""
		defined method.
		请求进入某个space中
		"""
		self._roomAllocs[spaceUType].teleportSpace(entityMailbox, position, direction, context)

	#--------------------------------------------------------------------------------------------
	#                              Callbacks
	#--------------------------------------------------------------------------------------------
	def onTimer(self, tid, userArg):
		"""
		KBEngine method.
		引擎回调timer触发
		"""
		#DEBUG_MSG("%s::onTimer: %i, tid:%i, arg:%i" % (self.getScriptName(), self.id, tid, userArg))
		if SCDefine.TIMER_TYPE_CREATE_SPACES == userArg:
			self.createSpaceOnTimer(tid)
		
		GameObject.onTimer(self, tid, userArg)
		
	def onSpaceLoseCell(self, spaceUType, spaceKey):
		"""
		defined method.
		space的cell创建好了
		"""
		self._roomAllocs[spaceUType].onSpaceLoseCell(spaceKey)
		
	def onSpaceGetCell(self, spaceKey,	context,playerA,playerB):
		"""
		defined method.
		space的cell创建好了
		"""
		self._roomAllocs[0].onSpaceGetCell( spaceKey,spaceMailbox,	context,playerA,playerB)

	

