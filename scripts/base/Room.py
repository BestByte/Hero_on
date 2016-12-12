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
		
		#self.spaceResName = d_spaces.datas.get(self.spaceUTypeB)['resPath']
		
		# 这个地图上创建的entity总数
		#self.tmpCreateEntityDatas = copy.deepcopy(d_spaces_spawns.datas.get(self.spaceUTypeB, ()))
		
		self.avatars = {}
		
	def teleportSpace(self, spaceKey, playerA, playerB, context):
		"""
		defined method.
		请求进入某个space中
		"""
		for mb, pos, dir in playerA:
			playerA.cell.onTeleportSpaceCB(self.cell, self.spaceKey, pos, dir)
			DEBUG_MSG("playerA.cell.onTeleportSpaceCB(self.id :%i, self.spaceKey:%i, pos=%s, dir=%s)"%(self.id, self.spaceKey, pos, dir))
		for mb, pos, dir in playerB:
			playerB.cell.onTeleportSpaceCB(self.cell, self.spaceKey, pos, dir)
			DEBUG_MSG("playerB.cell.onTeleportSpaceCB(self.id :%i, self.spaceKey:%i, pos=%s, dir=%s)"%(self.id, self.spaceKey, pos, dir))


	#---------------------------------------------------------------------
	#                              Callbacks
	#---------------------------------------------------------------------
	def onTimer(self, tid, userArg):
		"""
		KBEngine method.
		引擎回调timer触发
		"""
		#DEBUG_MSG("%s::onTimer: %i, tid:%i, arg:%i" % (self.getScriptName(), self.id, tid, userArg))
		
		GameObject.onTimer(self, tid, userArg)
		

	def onLoseCell(self):
		"""
		KBEngine method.
		entity的cell部分实体丢失
		"""
		KBEngine.globalData["rooms"].onSpaceLoseCell(self.spaceKey,
			self,							
											self.context,	
											self.matched_palyer,
											self.player_mailbox)
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

		

