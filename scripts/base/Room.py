# -*- coding: utf-8 -*-
import KBEngine
import random
import SCDefine
import copy
import math
from KBEDebug import *
from interfaces.GameObject import GameObject
import d_entities
import d_spaces
import d_spaces_spawns
import xml.etree.ElementTree as etree 

class Room(KBEngine.Base, GameObject):
	"""
	一个可操控cellapp上真正space的实体
	注意：它是一个实体，并不是真正的space，真正的space存在于cellapp的内存中，通过这个实体与之关联并操控space。
	"""
	def __init__(self,matched_player,player):
		KBEngine.Base.__init__(self)
		GameObject.__init__(self)

		#Space实体创建出来之后，此时还没有真正创建出空间， 这个实体仅仅是将要与某个真正空间关联的实体， 可以通过它来操控那个空间。

		#但空间只能在cellapp上存在， 因此我们需要调用API让实体在cell上创建出一个空间，并在cell上创建出一个实体与空间关联， 这个实体就像一个空间的句柄。

		#此功能由createInNewSpace完成, __init__可以理解为Space的构造函数。
		self.createInNewSpace(None)
		
		#self.spaceUTypeB = self.cellData["spaceUType"]
		
		self.spaceResName = d_spaces.datas.get(self.spaceUTypeB)['resPath']
		
		# 这个地图上创建的entity总数
		self.tmpCreateEntityDatas = copy.deepcopy(d_spaces_spawns.datas.get(self.spaceUTypeB, ()))
		
		self.avatars = {}
		self.createSpawnPointDatas()
		
	

	#等到引擎API函数onGetCell调用成功之后才负责
	#出生点的数据（实体类型、坐标、朝向等）是通过配置文件给出的，script/data/d_spaces_spawns.py与script/data/spawnpoints/xinshoucun_spawnpoints.xml 关于这2个配置的由来可以参考配置章节	
	def spawnOnTimer(self, tid):
		"""
		????????
		"""
		if len(self.tmpCreateEntityDatas) <= 0:
			self.delTimer(tid)
			return
			
		datas = self.tmpCreateEntityDatas.pop(0)
		
		if datas is None:
			ERROR_MSG("Space::onTimer: spawn %i is error!" % datas[0])

		KBEngine.createBaseAnywhere("SpawnPoint", 
									{"spawnEntityNO"	: datas[0], 	\
									"position"			: datas[1], 	\
									"direction"			: datas[2],		\
									"modelScale"		: datas[3],		\
									"createToCell"		: self.cell})
				
	def loginToSpace(self, avatarMailbox, context):
		"""
		defined method.
		某个玩家请求登陆到这个space中
		"""
		avatarMailbox.createCell(self.cell)
		self.onEnter(avatarMailbox)
		
	def logoutSpace(self, entityID):
		"""
		defined method.
		某个玩家请求登出这个space
		"""
		self.onLeave(entityID)
		
	def teleportSpace(self, spaceKey, playerA, playerB, context):
		"""
		defined method.
		请求进入某个space中
		"""
		for mb, pos, dir in playerA:
			playerA.cell.onTeleportSpaceCB(self.cell, self.spaceKey, pos, dir)
		for mb, pos, dir in playerB:
			playerB.cell.onTeleportSpaceCB(self.cell, self.spaceKey, pos, dir)

	#---------------------------------------------------------------------
	#                              Callbacks
	#---------------------------------------------------------------------
	def onTimer(self, tid, userArg):
		"""
		KBEngine method.
		引擎回调timer触发
		"""
		#DEBUG_MSG("%s::onTimer: %i, tid:%i, arg:%i" % (self.getScriptName(), self.id, tid, userArg))
		if SCDefine.TIMER_TYPE_SPACE_SPAWN_TICK == userArg:
			self.spawnOnTimer(tid)
		
		GameObject.onTimer(self, tid, userArg)
		
	def onEnter(self, entityMailbox):
		"""
		defined method.
		进入场景
		"""
		self.avatars[entityMailbox.id] = entityMailbox
		
		if self.cell is not None:
			self.cell.onEnter(entityMailbox)
		
	def onLeave(self, entityID):
		"""
		defined method.
		离开场景
		"""
		if entityID in self.avatars:
			del self.avatars[entityID]
		
		if self.cell is not None:
			self.cell.onLeave(entityID)

	def onLoseCell(self):
		"""
		KBEngine method.
		entity的cell部分实体丢失
		"""
		KBEngine.globalData["Spaces"].onSpaceLoseCell(self.spaceUTypeB, self.spaceKey)
		GameObject.onLoseCell(self)
		
	#onGetCell添加了一个刷出生点的定时器， 我们不能一次性创建出所有的出生点，因为数量可能很多, 使用定时器分批创建。

		#引擎API函数

		#如果这个函数在脚本中有实现，这个函数在它获得cell实体的时候被调用。这个函数没有参数。

	def onGetCell(self):
		"""
		KBEngine method.
		entity的cell部分实体被创建成功
		"""
		DEBUG_MSG("Space::onGetCell: %i" % self.id)
		self.addTimer(0.1, 0.1, SCDefine.TIMER_TYPE_SPACE_SPAWN_TICK)

		#注册space到spaces
		#KBEngine.globalData["Spaces"].onSpaceGetCell(self.spaceUTypeB, self, self.spaceKey)
		#GameObject.onGetCell(self)
	
		#注册room到match
		KBEngine.globalData["Rooms"].onSpaceGetCell(self.spaceKey,
			self,							
											self.context,	
											self.matched_palyer,
											self.player_mailbox)
		GameObject.onGetCell(self)

		

