from KBEDebug import *
import GlobalDefine
import KBEngine 
from interfaces.GameObject import GameObject
from interfaces.Teleport import Teleport
from interfaces.Spell import Spell
from interfaces.State import State
from interfaces.Motion import Motion
from interfaces.SkillBox import SkillBox
from interfaces.Combat import Combat
from interfaces.State import State
from interfaces.Dialog import Dialog
class Player(KBEngine.Entity,GameObject,Teleport,Motion,Spell,Combat,SkillBox,State,Dialog):
	def __init__(self):
		KBEngine.Enity.__init__(self)
		GameObject.__init__(self)
		State.__init__(self)
		Teleport.__init__(self)
		Motion.__init__(self)
		Combat.__init__(self)
		State.__init__(self)
		Dialog.__init__(self)

#---------------------------------------------------------------------------------
	#                              Callbacks
#-----------------------------------------------------------------------------
	def onTimer(self, tid, userArg):
		"""
		KBEngine method.
		引擎回调timer触发
		"""
		#DEBUG_MSG("%s::onTimer: %i, tid:%i, arg:%i" % (self.getScriptName(), self.id, tid, userArg))
		GameObject.onTimer(self, tid, userArg)
		Spell.onTimer(self, tid, userArg)
		
	def onGetWitness(self):
		"""
		KBEngine method.
		绑定了一个观察者(客户端)
		"""
		DEBUG_MSG("Avatar::onGetWitness: %i." % self.id)

	def onLoseWitness(self):
		"""
		KBEngine method.
		解绑定了一个观察者(客户端)
		"""
		DEBUG_MSG("Avatar::onLoseWitness: %i." % self.id)
	
	def onDestroy(self):
		"""
		KBEngine method.
		entity销毁
		"""
		DEBUG_MSG("Avatar::onDestroy: %i." % self.id)
		Teleport.onDestroy(self)
		Combat.onDestroy(self)
		
	

