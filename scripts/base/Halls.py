# -*- coding: utf-8 -*-
import KBEngine
import Functor
from KBEDebug import *
import traceback
import GameConfigs
from collections import deque
FIND_ROOM_NOT_FOUND = 0
FIND_ROOM_CREATING = 1

class Halls(KBEngine.Base):
	"""
	这是一个脚本层封装的房间管理器
	"""
	def __init__(self):
		KBEngine.Base.__init__(self)
		
		# 向全局共享数据中注册这个管理器的mailbox以便在所有逻辑进程中可以方便的访问
		KBEngine.globalData["Halls"] = self

		# 所有房间，是个字典结构，包含 {"roomMailbox", "PlayerCount", "enterRoomReqs"}
		# enterRoomReqs, 在房间未创建完成前， 请求进入房间和登陆到房间的请求记录在此，等房间建立完毕将他们扔到space中
		self.rooms = {}
		
        self.high_deque=deque()
        self.med_deque=deque()
        self.low_deque=deque()

		self.lastNewRoomKey = 0

		self.roomKey=0

		#每两秒检查一次需要匹配的玩家情况
        self.addTimer(1, 2, 1)

	def leaveRoom(self, avatarID, roomKey):
		"""
		defined method.
		某个玩家请求登出服务器并退出这个space
		"""
		roomDatas = self.findRoom(roomKey, False)

		if type(roomDatas) is dict:
			roomMailbox = roomDatas["roomMailbox"]
			if roomMailbox:
				roomMailbox.leaveRoom(avatarID)
		else:
			# 由于玩家即使是掉线都会缓存至少一局游戏， 因此应该不存在退出房间期间地图正常创建中
			if roomDatas == FIND_ROOM_CREATING:
				raise Exception("FIND_ROOM_CREATING")

    def matchRoom(self):
		while (len(self.high_deque)>2 or len(self.low_deque)>2 orlen(self.med_deque)>2):
				if len(self.high_deque)>2:
				    a_Mb=self.high_deque.pop()
				    b_Mb=self.high_deque.pop()
				
					#产生房间的key
					self.roomKey=KBEngine.genUUID64()
				
					# 将房间base实体创建在任意baseapp上
					# 此处的字典参数中可以对实体进行提前def属性赋值
					KBEngine.createBaseAnywhere("Room", \
									{
									"roomKey" : self.roomKey,	\
									}, \
									Functor.Functor(self.onRoomCreatedCB, self.roomKey))
			
					roomDatas = {"roomMailbox" : None, "PlayerCount": 0, "enterRoomReqs" : [], "roomKey" : self.roomKey}

					self.rooms[self.roomKey]=roomDatas	
					
					roomMailbox = roomDatas["roomMailbox"]

					#这样，两个匹配的玩家就就加入房间了
					roomDatas["enterRoomReqs"].append((a_Mb, position, direction))

					roomDatas["enterRoomReqs"].append((b_Mb, position, direction))


                elif len(self.med_deque)>2:
			       a_Mb=self.high_deque.pop()
				    b_Mb=self.high_deque.pop()
				
					#产生房间的key
					self.roomKey=KBEngine.genUUID64()
				
					# 将房间base实体创建在任意baseapp上
					# 此处的字典参数中可以对实体进行提前def属性赋值
					KBEngine.createBaseAnywhere("Room", \
									{
									"roomKey" : self.roomKey,	\
									}, \
									Functor.Functor(self.onRoomCreatedCB, self.roomKey))
			
					roomDatas = {"roomMailbox" : None, "PlayerCount": 0, "enterRoomReqs" : [], "roomKey" : self.roomKey}

					self.rooms[self.roomKey]=roomDatas	
					
					roomMailbox = roomDatas["roomMailbox"]

					#这样，两个匹配的玩家就就加入房间了
					roomDatas["enterRoomReqs"].append((a_Mb, position, direction))

					roomDatas["enterRoomReqs"].append((b_Mb, position, direction))
				
				 elif len(self.low_deque)>2:
			       a_Mb=self.high_deque.pop()
				    b_Mb=self.high_deque.pop()
				
					#产生房间的key
					self.roomKey=KBEngine.genUUID64()
				
					# 将房间base实体创建在任意baseapp上
					# 此处的字典参数中可以对实体进行提前def属性赋值
					roomMailbox=KBEngine.createBaseAnywhere("Room", \
									{
									"roomKey" : self.roomKey,	\
									}, \
									Functor.Functor(self.onRoomCreatedCB, self.roomKey))
			
					roomDatas = {"roomMailbox" : roomMailbox, "PlayerCount": 0, "enterRoomReqs" : [], "roomKey" : self.roomKey}

					self.rooms[self.roomKey]=roomDatas	
					
					roomMailbox = roomDatas["roomMailbox"]

					#这样，两个匹配的玩家就就加入房间了
					roomDatas["enterRoomReqs"].append((a_Mb, position, direction))

					roomDatas["enterRoomReqs"].append((b_Mb, position, direction))
	

			
	#--------------------------------------------------------------------------------------------
	#                              Callbacks
	#--------------------------------------------------------------------------------------------
	def onRoomCreatedCB(self, roomKey, roomMailbox):
		"""
		一个space创建好后的回调
		"""
		DEBUG_MSG("Halls::onRoomCreatedCB: space %i. entityID=%i" % (roomKey, roomMailbox.id))

	def onTimer(self, tid, userArg):
		"""
		KBEngine method.
		引擎回调timer触发
		"""
		#DEBUG_MSG("%s::onTimer: %i, tid:%i, arg:%i" % (self.getScriptName(), self.id, tid, userArg))
		if userArg==1 and len(self.high_deque)>2 and len(self.high_deque)>2:
			self.high_match()
		GameObject.onTimer(self, tid, userArg)
		
	def onRoomLoseCell(self, roomKey):
		"""
		defined method.
		Room的cell销毁了
		"""
		DEBUG_MSG("Halls::onRoomLoseCell: space %i." % (roomKey))
		del self.rooms[roomKey]

	def onRoomGetCell(self, roomMailbox, roomKey):
		"""
		defined method.
		Room的cell创建好了
		"""
		self.rooms[roomKey]["roomMailbox"] = roomMailbox

		# space已经创建好了， 现在可以将之前请求进入的玩家全部丢到cell地图中
		for infos in self.rooms[roomKey]["enterRoomReqs"]:
			entityMailbox = infos[0]
			entityMailbox.createCell(roomMailbox.cell)
			
		self.rooms[roomKey]["enterRoomReqs"] = []