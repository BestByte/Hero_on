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

class Master(KBEngine.Base, GameObject):
	"""
	
	"""
	def __init__(self):
		KBEngine.Base.__init__(self)
		GameObject.__init__(self)

		#��Ҫƥ�������Ҽ���
		self.playerMactch={}
		#���е�����PVP��ս�����Ҽ���

		#Master�����ľ���ȷ�ϵĸ���ʵ��
		self.playerCal={}
	
		
		KBEngine.globalData["Master"] = self
		DEBUG_MSG("KBEngine.globalData[Master]")

	def addPVPMatch(self,player):
		"""
		defined method.

		player:MailBox
		player_match_num:Match���ڵ�baseAPP����

		Ŀǰϵͳ���漰baseapp5��������1��2ר�Ÿ���matchƥ��ʵ�壬3����rooms��������ʵ�壬3��4��5����playerʵ�塢room����ʵ��
		""" 
		DEBUG_MSG("Match[%i].addPVPMatch" % int(os.getenv("KBE_BOOTIDX_GROUP")))
		
		#��Master�Ͻ���������match���ܵ�ƥ������
		self.playerMactch[player.id]=player

		#��Master�Ͻ���������match���ܵ�ƥ������
		self.playerCal[player.id]={}

		#改为单个baseapp后更改的，若多个baseapp之后，直接删除下面，把下面的注释的重新取消注释即可
		"""
		for x in range(4):
			KBEngine.globalData["match%i"% (x+2)].eachPVPMatch(player)
		"""
		KBEngine.globalData["match1"].eachPVPMatch(player)

	def addPVPResult(self,matchedPlayer,matchedChampion, player,playerChampion,match_order):#match_order ��match������ֵ

		#��matchʵ�����ܴ���
		#���ǵ�baseapp��˳��match_order
		self.playerCal[player.id][match_order]=matchedPlayer

		

		#改为单个baseapp后更改的，若多个baseapp之后，直接删除下面，把下面的注释的重新取消注释即可
		"""
		if self.playerCal[player.id].__len__()==4:
			cal_result(player_match_number)
		"""
		if self.playerCal[player.id].__len__()==1:
			cal_result(player_match_number)
	
	def cal_result(self,player_match_number):
		end_palyer=None
		
		min_val=30
		match_num=0 #��С���������ڵ�baseapp
		#改为单个baseapp后更改的，若多个baseapp之后，直接删除下面，把下面的注释的重新取消注释即可
		"""
		for k ,v in self.playerCal[player.id].items():
			if v !=None:
				if min_val>abs(self.reqGetAttrs(v)-self.reqGetAttrs(player)):
					min_val=abs(self.reqGetAttrs(v)-self.reqGetAttrs(player))
					end_palyer=v
					match_num=k
		"""
		for k ,v in self.playerCal[player.id].items():
			if v !=None:
				if min_val>abs(v.champion-palyer.champion):
					min_val=abs(v.champion-palyer.champion)
					end_palyer=v
					match_num=k
		#�����Ǹ���ѡ����������ʵ�壬��������
		KBEngine.globalData["Rooms"].createSpace(0,{},self.playerCal[player.id][k], player)

		
		"""
		del self.playerCal[player.id]
		del KBEngine.globalData["match%i"%player_match_number].playerMatch[player.id]
		del KBEngine.globalData["Master"].playerMatch[end_palyer.id]
		"""
		#改为单个baseapp后更改的，若多个baseapp之后，直接删除下面，把下面的注释的重新取消注释即可
		del self.playerCal[player.id]
		del KBEngine.globalData["match1"].playerMatch[player.id]
		del KBEngine.globalData["Master"].playerMatch[end_palyer.id]

	#-----------------------------------------------------------
	#                              Callbacks
	#-----------------------------------------------------------
	def onTimer(self, tid, userArg):
		"""
		KBEngine method.
		引擎回调timer触发
		"""
		#DEBUG_MSG("%s::onTimer: %i, tid:%i, arg:%i" % (self.getScriptName(), self.id, tid, userArg))
		
		GameObject.onTimer(self, tid, userArg)

	

