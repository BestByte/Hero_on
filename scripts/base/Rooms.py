# -*- coding: utf-8 -*-
import KBEngine
import Functor
import d_spaces
import SCDefine
import Watcher
from KBEDebug import *

from interfaces.GameObject import GameObject

class Rooms(KBEngine.Base, GameObject):
	"""
	这是一个脚本层封装的房间（room）管理器
	KBEngine的space是一个抽象空间的概念，一个空间可以被脚本层视为游戏场景、游戏房间、甚至是一个宇宙。
	"""
	def __init__(self):
		KBEngine.Base.__init__(self)
		GameObject.__init__(self)
		
		
		
		# 将自己注册到共享数据中， 在当前进程KBEngine.globalData["Halls"]返回的是Halls实体，其他进程中,由于实体不在那个进程所以KBEngine.globalData["Halls"]返回的是mailbox
		# 因此调用KBEngine.globalData["Halls"].xxx方法必须在def定义，允许远程访问

		# 向全局共享数据中注册这个管理器的mailbox以便在所有逻辑进程中可以方便的访问
		KBEngine.globalData["Rooms"] = self

	# 这里真正开始创建这些space实体， 里面调用的createBaseAnywhere函数来创建实体， 如果启动了多个baseapp这个函数根据负载情况将实体选择到合适的进程中创建。	
	def createSpace(self, spaceKey, context,matched_player,player_mailbox):
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
											"matched_player":matched_player, "player_mailbox":player_mailbox
											}, \
											Functor.Functor(self.onSpaceCreatedCB, spaceKey,player_mailbox,matched_player))

	def onSpaceCreatedCB(self, spaceKey,player_mailbox,matched_player, space):
		"""
		一个space创建好后的回调
		"""
		DEBUG_MSG("Rooms::onSpaceCreatedCB: room spaceKey [%i]. spaceID=[%i]" % (spaceKey, space.id))

		player_mailbox.client.on_match_success("匹配成功")
		DEBUG_MSG("player_mailbox.client.on_match_success(匹配成功) room spaceKey [%i]. spaceID=[%i]" % (spaceKey, space.id))
		matched_player.client.on_match_success("匹配成功")
		DEBUG_MSG("matched_player.client.on_match_success(匹配成功): room spaceKey [%i]. spaceID=[%i]" % (spaceKey, space.id))

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
		
	def onSpaceLoseCell(self, spaceKey,	
											room_base_mailbox,
											context,
											matched_palyer,
											player_mailbox):
		"""
		defined method.
		space的cell创建好了
		"""

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

