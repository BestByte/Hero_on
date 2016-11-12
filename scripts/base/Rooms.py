# -*- coding: utf-8 -*-
import KBEngine
import Functor
import d_spaces
import SCDefine
import Watcher
from KBEDebug import *
from SpaceAlloc import *
from interfaces.GameObject import GameObject

class Rooms(KBEngine.Base, GameObject):
	"""
	这是一个脚本层封装的房间（room）管理器
	KBEngine的space是一个抽象空间的概念，一个空间可以被脚本层视为游戏场景、游戏房间、甚至是一个宇宙。
	"""
	def __init__(self):
		KBEngine.Base.__init__(self)
		GameObject.__init__(self)
		
		# 初始化空间分配器
		self.initAlloc()
		
		# 将自己注册到共享数据中， 在当前进程KBEngine.globalData["Halls"]返回的是Halls实体，其他进程中,由于实体不在那个进程所以KBEngine.globalData["Halls"]返回的是mailbox
		# 因此调用KBEngine.globalData["Halls"].xxx方法必须在def定义，允许远程访问

		# 向全局共享数据中注册这个管理器的mailbox以便在所有逻辑进程中可以方便的访问
		KBEngine.globalData["Rooms"] = self

	# 这里真正开始创建这些space实体， 里面调用的createBaseAnywhere函数来创建实体， 如果启动了多个baseapp这个函数根据负载情况将实体选择到合适的进程中创建。	
	def createSpace(self, spaceKey, context,matched_palyer,palyer_mailbox):
		"""
		"""
		if spaceKey <= 0:
			spaceKey = KBEngine.genUUID64()
			
		context = copy.copy(context)
		#spaceData = d_spaces.datas.get(self._utype)
		KBEngine.createBaseAnywhere("Room", \
											{
											"spaceKey" : spaceKey,	\
											"context" : context,	\
											"matched_player":matched_palyer, "player_mailbox":palyer_mailbox
											}, \
											Functor.Functor(self.onSpaceCreatedCB, spaceKey))

	def onSpaceCreatedCB(self, spaceKey, space):
		"""
		一个space创建好后的回调
		"""
		DEBUG_MSG("Rooms::onSpaceCreatedCB: room spaceKey [%i]. spaceID=[%i]" % (spaceKey, space.id))
		
	def initAlloc(self):

		# 注册一个定时器，在这个定时器中我们每个周期都创建出一些场景，直到创建完所有
		self._spaceAllocs = {}
		self.addTimer(3, 1, SCDefine.TIMER_TYPE_CREATE_SPACES)
		
		self._tmpDatas = list(d_spaces.datas.keys())
		for utype in self._tmpDatas:
			spaceData = d_spaces.datas.get(utype)
			if spaceData["entityType"] == "SpaceDuplicate":
				self._spaceAllocs[utype] = SpaceAllocDuplicate(utype)
			else:
				self._spaceAllocs[utype] = SpaceAlloc(utype)
	
	def getSpaceAllocs(self):
		return self._spaceAllocs
		
	def createSpaceOnTimer(self, tid):
		"""
		创建space
		这个定时器下面才是真正才能场景的，前面的__init__()只是初始化
		"""
		if len(self._tmpDatas) > 0:
			spaceUType = self._tmpDatas.pop(0)
			self._spaceAllocs[spaceUType].init()
			
		if len(self._tmpDatas) <= 0:
			del self._tmpDatas
			self.delTimer(tid)
			
	def loginToSpace(self, avatarEntity, spaceUType, context):
		"""
		defined method.
		某个玩家请求登陆到某个space中
		"""
		self._spaceAllocs[spaceUType].loginToSpace(avatarEntity, context)
	
	def logoutSpace(self, avatarID, spaceKey):
		"""
		defined method.
		某个玩家请求登出这个space
		"""
		for spaceAlloc in self._spaceAllocs.values():
			space = spaceAlloc.getSpaces().get(spaceKey)
			if space:
				space.logoutSpace(avatarID)
				
	def teleportSpace(self, entityMailbox, spaceUType, position, direction, context):
		"""
		defined method.
		请求进入某个space中
		"""
		self._spaceAllocs[spaceUType].teleportSpace(entityMailbox, position, direction, context)

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
		self._spaceAllocs[spaceUType].onSpaceLoseCell(spaceKey)
		
	def onSpaceGetCell(self, spaceKey,	
											room_base_mailbox,
											context,
											matched_palyer,
											player_mailbox):
		"""
		defined method.
		space的cell创建好了
		"""
		room_base_mailbox.teleportSpace(spaceKey, matched_palyer, player_mailbox, context)

