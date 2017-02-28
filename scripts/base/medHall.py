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

		#???Ÿ?ս???????ҵ?dequeue
		self.med_deque=deque()
		
		KBEngine.globalData["highHall"] = self
		DEBUG_MSG("KBEngine.globalData[highHall]")

		self.addTimer(1, 0, 1)

	def high_match(self):
		while True:
			if len(self.med_deque)>2:
				a_Mb=self.med_deque.pop()
				b_Mb=self.med_deque.pop()
				KBEngine.globalData["Rooms"].createSpace(KBEngine.genUUID64(),{},a_Mb,b_Mb)

	#-----------------------------------------------------------
	#                              Callbacks
	#-----------------------------------------------------------
	def onTimer(self, tid, userArg):
		"""
		KBEngine method.
		?????ص?timer????
		"""
		#DEBUG_MSG("%s::onTimer: %i, tid:%i, arg:%i" % (self.getScriptName(), self.id, tid, userArg))
		if userArg==1:
			self.high_match()
		GameObject.onTimer(self, tid, userArg)

	

