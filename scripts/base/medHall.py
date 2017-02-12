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
from collections import *

class medHall(KBEngine.Base, GameObject):
	"""
	"""
	def __init__(self):
		KBEngine.Base.__init__(self)
		GameObject.__init__(self)

		#��Ÿ�ս������ҵ�dequeue
		self.med_deque=deque()
		
		KBEngine.globalData["highHall"] = self
		DEBUG_MSG("KBEngine.globalData[highHall]")

		self.addTimer(1, 0, 1)

	def high_match(self):
		while True:
			if len(self.med_deque)>2:
				a_Mb=self.med_deque.pop()
				b_Mb=self.med_deque.pop()
				KBEngine.createBaseAnywhere("Room", \
											{
											"spaceKey" : KBEngine.genUUID64(),	\
											"matched_player":a_Mb, \
											"player_mailbox":b_Mb
											}, \
											Functor.Functor(self.onSpaceCreatedCB, spaceKey,player_mailbox,matched_player))

	def onSpaceCreatedCB(self, spaceKey,player_mailbox,matched_player, space):
		"""
		һ��space�����ú�Ļص�
		"""
		DEBUG_MSG("Rooms::onSpaceCreatedCB: room spaceKey [%i]. spaceID=[%i]" % (spaceKey, space.id))

		player_mailbox.client.on_match_success("ƥ��ɹ�")
		DEBUG_MSG("player_mailbox.client.on_match_success(ƥ��ɹ�) room spaceKey [%i]. spaceID=[%i]" % (spaceKey, space.id))
		matched_player.client.on_match_success("ƥ��ɹ�")
		DEBUG_MSG("matched_player.client.on_match_success(ƥ��ɹ�): room spaceKey [%i]. spaceID=[%i]" % (spaceKey, space.id))

	#-----------------------------------------------------------
	#                              Callbacks
	#-----------------------------------------------------------
	def onTimer(self, tid, userArg):
		"""
		KBEngine method.
		����ص�timer����
		"""
		#DEBUG_MSG("%s::onTimer: %i, tid:%i, arg:%i" % (self.getScriptName(), self.id, tid, userArg))
		if userArg==1:
			self.high_match()
		GameObject.onTimer(self, tid, userArg)

	

