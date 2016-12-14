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
	����һ��ƥ��ϵͳ
	���ͻ��˵�¼ʱ��PVPģʽ�£�����PVP������
	ƥ��ϵͳ�������ߵ�champion�÷�����ʱƥ�䴴��space
	KBEngine��space��һ�������ռ��ĸ��һ���ռ����Ա��ű�����Ϊ��Ϸ��������Ϸ���䡢������һ�����档
	"""
	def __init__(self):
		KBEngine.Base.__init__(self)
		GameObject.__init__(self)

		#��Ҫƥ�������Ҽ���
		self.playerMactch={}
		#���е�����PVP��ս�����Ҽ���

		#Master�����ľ���ȷ�ϵĸ���ʵ��
		self.playerCal={}
	
		# ���Լ�ע�ᵽ���������У� �ڵ�ǰ����KBEngine.globalData["Halls"]���ص���Hallsʵ�壬����������
		# ����ʵ�岻���Ǹ���������KBEngine.globalData["Halls"]���ص���mailbox
		# ���˵���KBEngine.globalData["Halls"].xxx����������def���壬����Զ�̷���

		# ��ȫ�ֹ���������ע��������������mailbox�Ա��������߼������п��Է����ķ���
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

		for x in range(4):
			KBEngine.globalData["match%i"% (x+2)].eachPVPMatch(player)


	def addPVPResult(self,matchedPlayer,matchedChampion, player,playerChampion,match_order):#match_order ��match������ֵ

		#��matchʵ�����ܴ���
		#���ǵ�baseapp��˳��match_order
		self.playerCal[player.id][match_order]=matchedPlayer

		#�������е�matchϵͳ���Ѿ�������ƥ��ֵ��������������ѡ
		if self.playerCal[player.id].__len__()==4:
			cal_result(player_match_number)

	#���յ�ƥ�亯��	
	def cal_result(self,player_match_number):
		end_palyer=None
		
		min_val=30
		match_num=0 #��С���������ڵ�baseapp
		for k ,v in self.playerCal[player.id].items():
			if v !=None:
				if min_val>abs(self.reqGetAttrs(v)-self.reqGetAttrs(player)):
					min_val=abs(self.reqGetAttrs(v)-self.reqGetAttrs(player))
					end_palyer=v
					match_num=k

		#�����Ǹ���ѡ����������ʵ�壬��������
		KBEngine.globalData["Rooms"].createSpace(0,{},self.playerCal[player.id][k], player)

		#ѡ��������֮�󣬰������ֵ�ɾ���ˡ�
		#�и����⣬�᲻��ɾ��̫���ˣ�

		del self.playerCal[player.id]
		del KBEngine.globalData["match%i"%player_match_number].playerMatch[player.id]
		del KBEngine.globalData["Master"%k].playerMatch[end_palyer.id]

		#roomID=int(time.time()*100)

		#self.reqEnterRoom(self, roomID,self.playerMactch[player][x], player)
	#-----------------------------------------------------------
	#                              Callbacks
	#-----------------------------------------------------------
	def onTimer(self, tid, userArg):
		"""
		KBEngine method.
		???????��timer??��?
		"""
		#DEBUG_MSG("%s::onTimer: %i, tid:%i, arg:%i" % (self.getScriptName(), self.id, tid, userArg))
		
		GameObject.onTimer(self, tid, userArg)

	

