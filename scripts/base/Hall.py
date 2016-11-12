# -*- coding: utf-8 -*-
import KBEngine
import random
import time
import d_halls
import GlobalConst
from KBEDebug import *
from Room import *
import os						
class Hall(KBEngine.Base):
	"""
	大厅实体
	该实体管理该大厅中所有的房间/桌
	每个baseapp都有一个大厅
	"""
	def __init__(self):
		KBEngine.Base.__init__(self)
		
		# 向大厅管理器注册自己 
		#KBEngine.globalData["Halls"].addHall(self.hallID, self)
		
		# 存放所有房间信息
		self.rooms = {}
		
		# 通过添加一个定时器延时执行大厅的创建，确保一些状态在此期间能够初始化完毕
		self.addTimer(3, 0, 1)
		
		# 进入该大厅的所有玩家mailbox
		self.players = {}
		# 向全局共享数据中注册这个管理器的mailbox以便在所有逻辑进程中可以方便的访问
		KBEngine.globalData['hall%i'%(os.getenv("KBE_BOOTIDX_GROUP"))] = self
		
	def _createRooms(self):
		"""
		根据配置创建出所有的大厅
		"""
		for i in range(d_halls.datas[self.hallID]["roomCount"]):
			roomID = self.hallID * 1000 + i
			self.rooms[roomID] = Room(roomID, str(roomID))
													
	def onDestroy(self):
		KBEngine.globalData["Halls"].removeHall(self.hallID)
		
	def onTimer(self, id, userArg):
		"""
		KBEngine method.
		使用addTimer后， 当时间到达则该接口被调用
		@param id		: addTimer 的返回值ID
		@param userArg	: addTimer 最后一个参数所给入的数据
		"""
		DEBUG_MSG(id, userArg)

		if userArg == 1:
			self._createRooms()

	def addPVPMatch(self,player):
		#player is mailbox
		charge_value=100 #起始设定的与玩家奖杯的差值
		charge_id=1 #记录玩家的标号
		for x in self.players.values():
			#若是玩家正在匹配中，则状态码为2

		    if x.state==2:
				#若是在线的正要匹配的玩家当中，与匹配的玩家的奖杯数差值最少的玩家
				#则要传给baseapp1的匹配实体Match
			if charge_value<abs(x.champion-self.reqGetAttrs(player)):
					charge_value=abs(x.champion-self.reqGetAttrs(player))
					charge_id=x.id #记录最小差值玩家的标号
		if KBEngine.entities.has_key(charge_id):
			matchedPlayer=KBEngine.entities[charge_id]

		KBEngine.globalData["Match"].addPVPResult(matchedPlayer,matchedPlayer.champion,plalyer,self.reqGetAttrs(player))

	def reqGetAttrs(self, mailbox):
		mailbox.onGetAttr(self.attrs)	
			
	def reqEnumHall(self, player):
		"""
		defined.
		客户端调用该接口请求枚举列出所有大厅
		"""
		DEBUG_MSG("Hall[%i].reqEnumHall" % (self.id))
			
		results = []
		
		# 将数据按照HALL_INFOS_LIST类型返回， 参考alias.xml
		results.append({"rooms_count" : len(self.rooms), "players_count" : len(self.players), "id" : self.hallID, "name" : d_halls.datas[self.hallID]["hallName"]})

		player.client.onEnumHalls(results)
				
	def reqEnumRooms(self, player):
		"""
		defined.
		客户端调用该接口请求枚举列出所有房间/桌子
		"""
		DEBUG_MSG("Hall.reqEnumRooms: %s" % (player.id))
		roomList = []
		
		# 如果房间过多，应该分批下发，一次性下发将会瞬间数据量过大
		for room in self.rooms.values():
			roomList.append({"id" : room.roomID, "name" : room.roomName, "players_count" : len(room.players), "state" : room.state})
			
		player.client.onEnumRooms(roomList)
		
	def reqEnterHall(self, player):
		"""
		defined.
		客户端调用该接口请求进入大厅
		"""
		DEBUG_MSG("Hall.reqEnterHall: %s" % (player.id))
		# 应该在这里做一些条件，允许进入后返回给角色进入成功
		
		# 如果需要记录该大厅上的人也可以在此做记录
		#记录的是player的ID
		self.players[player.id] = player
		
	def reqLeaveHall(self, player):
		"""
		defined.
		客户端调用该接口请求离开大厅
		"""
		DEBUG_MSG("Hall.reqLeaveHall: %s" % (player.id))
		# 应该在这里做一些条件，允许进入后返回给角色离开成功
		del self.players[player.id]
		
	def reqEnterRoom(self, player, roomID):
		"""
		defined.
		客户端调用该接口请求进入房间/桌子
		"""
		DEBUG_MSG("Hall.reqEnterHall: %s" % (player.id))
		self.rooms[roomID].reqEnterRoom(player)
		
	def reqLeaveRoom(self, player, roomID):
		"""
		defined.
		客户端调用该接口请求离开房间/桌子
		"""
		DEBUG_MSG("Hall.reqLeaveRoom: %s" % (player.id))
		self.rooms[roomID].reqLeaveRoom(player)
		
	def reqStartGame(self, player, roomID):
		"""
		defined.
		客户端调用该接口请求开始游戏
		"""
		DEBUG_MSG("Hall.reqStartGame: %s" % (player.id))
		self.rooms[roomID].reqStartGame(player)
		
	def reqStopGame(self, player, roomID):
		"""
		defined.
		客户端调用该接口请求停止游戏
		"""
		DEBUG_MSG("Hall.reqStopGame: %s" % (player.id))
		self.rooms[roomID].reqStopGame(player)
						
	def say(self, player, roomID, str):
		"""
		defined.
		说话的内容
		"""
		DEBUG_MSG("Hall.say: %s" % (player.id))
		
		# 如果房间ID大于0说明玩家在房间中，那么只需要在房间内说话
		# 否则广播给大厅所有人(包含房间内的人)，将来使用大厅广播也许还会有喇叭等功能，那需要附带其他信息决定如何广播
		if roomID > 0:
			self.rooms[roomID].say(player, str)
		else:
			for mb in self.players.values():
				mb.client.onSay(str)			