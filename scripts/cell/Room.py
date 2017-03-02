# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
import GameConfigs
import random
import GameUtils

TIMER_TYPE_DESTROY = 1
TIMER_TYPE_BALANCE_MASS = 2

class Room(KBEngine.Entity):
	"""
	游戏场景
	"""
	def __init__(self):
		KBEngine.Entity.__init__(self)
		
		# 把自己移动到一个不可能触碰陷阱的地方
		#self.position = (999999.0, 0.0, 0.0)

		# 这个房间中所有的玩家
		self.avatars = {}
		
		
		
		# 告诉客户端加载地图
		KBEngine.addSpaceGeometryMapping(self.spaceID, None, "spaces/gameMap")
		
		DEBUG_MSG('created space[%d] entityID = %i, res = %s.' % (self.roomKeyC, self.id, "spaces/castle"))
		
		# 让baseapp和cellapp都能够方便的访问到这个房间的mailbox
		KBEngine.globalData["Room_%i" % self.spaceID] = self.base
	
		# 设置房间必要的数据，客户端可以获取之后做一些显示和限制
		KBEngine.setSpaceData(self.spaceID, "GAME_MAP_SIZE",  str(GameConfigs.GAME_MAP_SIZE))
		KBEngine.setSpaceData(self.spaceID, "ROOM_MAX_PLAYER",  str(GameConfigs.ROOM_MAX_PLAYER))
		KBEngine.setSpaceData(self.spaceID, "GAME_ROUND_TIME",  str(GameConfigs.GAME_ROUND_TIME))
		
	
			
	#--------------------------------------------------------------------------------------------
	#                              Callbacks
	#--------------------------------------------------------------------------------------------
	def onTimer(self, id, userArg):
		"""
		KBEngine method.
		使用addTimer后， 当时间到达则该接口被调用
		@param id		: addTimer 的返回值ID
		@param userArg	: addTimer 最后一个参数所给入的数据
		"""
		if TIMER_TYPE_DESTROY == userArg:
			self.onDestroyTimer()
		elif TIMER_TYPE_BALANCE_MASS == userArg:
			self.balanceMass()

	def onDestroy(self):
		"""
		KBEngine method.
		"""
		DEBUG_MSG("Room::onDestroy: %i" % (self.id))
		del KBEngine.globalData["Room_%i" % self.spaceID]
		
	
		
	def onEnter(self, entityMailbox):
		"""
		defined method.
		进入场景
		"""
		DEBUG_MSG('Room::onEnter space[%d] entityID = %i.' % (self.spaceID, entityMailbox.id))
		self.avatars[entityMailbox.id] = entityMailbox

	def onLeave(self, entityID):
		"""
		defined method.
		离开场景
		"""
		DEBUG_MSG('Room::onLeave space[%d] entityID = %i.' % (self.spaceID, entityID))
		
		if entityID in self.avatars:
			del self.avatars[entityID]

