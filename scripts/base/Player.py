# -*- coding: utf-8 -*-
import KBEngine
import time
import d_spaces
import GlobalConst
from interfaces.GameObject import GameObject
from interfaces.Teleport import Teleport
import math
from KBEDebug import *
import random
class Player(KBEngine.Proxy,GameObject):
	"""
	账号实体
	客户端登陆到服务端后，服务端将自动创建这个实体，通过这个实体与客户端进行交互
	"""
	def __init__(self):
		KBEngine.Proxy.__init__(self)
		
		# 状态0：未开始游戏， 1：游戏中,2:匹配中，3.上线
		#考虑做个def中的存储
		#self.state = 0
		self.relogin = time.time()
		self.cellData["dbid"] = self.databaseID
		#Player创建完成之后自动加入大厅
		#KBEngine.globalData["Hall"].reqEnterHall(self)

	def req_match(self):
		"""
		exposed

		defined method.
		客户端请求匹配
		"""
		DEBUG_MSG("Player[%i].req_match" % (self.id))
		
		#考虑增加对于反复点击匹配的问题，检测deque里是否有玩家，若有的话则不再往deque里添加了。
		KBEngine.globalData["Halls"].addDeque(self,int(self.champion))
		
		DEBUG_MSG("player [%d]:req_match(self)"%self.id )
		self.client.on_req_match("正在匹配中...")

	def func(self):
		"""
		defined method
		"""
		#改为单个baseapp后更改的，若多个baseapp之后，直接删除下面，把下面的注释的重新取消注释即可
         # 请求获取match的属性
		"""
		for i in range(4):
			KBEngine.globalData["match%i"%(i+2)].reqGetAttrs(self)# // 注意：这里将自己传入方法了， 引擎会将其转变为mailbox传输到对方进程上并传入这个实体的方法中， 在spaces中就可以将信息返回给指定实体了。
		DEBUG_MSG("KBEngine.globalData[match%i]:reqGetAttrs(self)")
		"""
		KBEngine.globalData["match1"].reqGetAttrs(self)

	def onGetAttr(self):
		"""
		defined method.
		"""
		return self.champion

		DEBUG_MSG("Player[%i].self.champion[%i]" % (self.id,self.champion))

	def createCell(self, space):
		"""
		defined method.
		创建cell实体
		"""
		self.createCellEntity(space)
	
	def attack(self,exposed,type):
		'''
		defined method.
		攻击
		'''
		#若是将来考虑延时的时候，做一个一次性的定时器，目前看也能达到类似的效果
		if exposed !=self.id:
			return

		DEBUG_MSG("Avatar::attack: %i, type=%i." % (self.id, type))

		#通过modelID这样，客户端在onenterworld中加载不同的额模型
		params={
			"modelID":type
		}

		e=KBEngine.createEntity("Monster",self,spaceID,tuple(self.position),tuple(self.direction),params)

	#-------------------------------------------------
	#						Callbacks
	#-------------------------------------------------

	def onEntitiesEnabled(self):
		"""
		KBEngine method.
		该entity被正式激活为可使用， 此时entity已经建立了client对应实体， 可以在此创建它的
		cell部分。
		"""
		INFO_MSG("Account[%i]::onEntitiesEnabled:entities enable. mailbox:%s, clientType(%i), clientDatas=(%s), accountName=%s" % \
			(self.id, self.client, self.getClientType(), self.getClientDatas(), self.__ACCOUNT_NAME__))
		

	def onLogOnAttempt(self, ip, port, password):
		"""
		KBEngine method.
		客户端登陆失败时会回调到这里
		"""
		INFO_MSG("Account[%i]::onLogOnAttempt: ip=%s, port=%i, selfclient=%s" % (self.id, ip, port, self.client))
	
		# 如果一个在线的账号被一个客户端登陆并且onLogOnAttempt返回允许
		# 那么会踢掉之前的客户端连接
		# 那么此时self.activeAvatar可能不为None， 常规的流程是销毁这个角色等新客户端上来重新选择角色进
		return KBEngine.LOG_ON_ACCEPT
		
	def onClientDeath(self):
		"""
		KBEngine method.
		客户端对应实体已经销毁
		"""
		DEBUG_MSG("Account[%i].onClientDeath:" % self.id)
		self.destroy()		
		
	