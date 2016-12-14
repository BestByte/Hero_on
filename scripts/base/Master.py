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
	���ͻ��˵�¼ʱ��PVPģʽ�£�����PVP����
	ƥ��ϵͳ������ߵ�champion�÷����ʱƥ�䴴��space
	KBEngine��space��һ������ռ�ĸ��һ���ռ���Ա��ű�����Ϊ��Ϸ��������Ϸ���䡢������һ�����档
	"""
	def __init__(self):
		KBEngine.Base.__init__(self)
		GameObject.__init__(self)

		#?��????????????????
		self.playerMactch={}
		#?��???????��PVP??????????????

		#match1 ?��???????��?��?????��??????
		self.playerCal={}
		#self.players={}
		
	

		# ���Լ�ע�ᵽ���������У� �ڵ�ǰ����KBEngine.globalData["Halls"]���ص���Hallsʵ�壬����������
		# ����ʵ�岻���Ǹ���������KBEngine.globalData["Halls"]���ص���mailbox
		# ��˵���KBEngine.globalData["Halls"].xxx����������def���壬����Զ�̷���

		# ��ȫ�ֹ���������ע�������������mailbox�Ա��������߼������п��Է���ķ���
		KBEngine.globalData["Master"] = self
		DEBUG_MSG("KBEngine.globalData[Master]")

		

	def addPVPMatch(self,player,player_match_num):
		"""
		defined method.

		player:MailBox
		player_match_num:Match���ڵ�baseAPP���

		Ŀǰϵͳ���漰baseapp5��������1��2ר�Ÿ���matchƥ��ʵ�壬3����rooms��������ʵ�壬3��4��5����playerʵ�塢room����ʵ��
		""" 
		DEBUG_MSG("Match[%i].addPVPMatch" % int(os.getenv("KBE_BOOTIDX_GROUP")))
		
		#��match1�Ͻ���������match���ܵ�ƥ������
		self.playerMactch[player.id]=player

		#��match1�Ͻ���������match���ܵ�ƥ������
		KBEngine.globalData["Master"].playerCal[player.id]={}

		for x in range(4):
			KBEngine.globalData["match%i"% (x+2)].eachPVPMatch(player,player_match_num)

		#self.charge_value=100#?????��?��?????????����???????

	def eachPVPMatch(self,player,player_match_number):
		"""
		player:MailBox
		player_match_num:Match?��????baseAPP����??
		""" 
		charge_value=200 #?????��?��?????????����???????
		charge_id=1 #??????????����??
		for x in self.playerMactch.values():
			
				#?????????????????????????��???????????????????����???????��?????????
				#?��??????baseapp1??????????Match
				#x????��??????????????��??��???champion????
			if charge_value<abs(x.champion-self.reqGetAttrs(player)) and x.id != player.id:#????????????????????????????
					charge_value=abs(x.champion-self.reqGetAttrs(player))
					charge_id=x.id #????��?????????????����??
			else:
				charge_value=abs(x.champion-self.reqGetAttrs(player))
				charge_id=x.id
		if KBEngine.entities.has_key(charge_id):
			matchedPlayer=KBEngine.entities[charge_id]
		else:
			matchedPlayer=None

			#?��match???��
		KBEngine.globalData["match1"].addPVPResult(matchedPlayer,matchedPlayer.champion,plalyer,self.reqGetAttrs(player),player_match_number,int(os.getenv("KBE_BOOTIDX_GROUP")))

		DEBUG_MSG("KBEngine.globalData['match1'].addPVPResult(matchedPlayer[%s],matchedPlayer.champion[%i],plalyer[%s],self.reqGetAttrs(player,champion)[%i]),os.getenv('KBE_BOOTIDX_GROUP')[%i]" % (matchedPlayer,matchedPlayer.champion,plalyer,self.reqGetAttrs(player),int(os.getenv("KBE_BOOTIDX_GROUP"))))

	def reqGetAttrs(self, mailbox):
		mailbox.onGetAttr(self.champion)
		DEBUG_MSG("Player[%i].reqGetAttr(self, mailbox,attrs [%s]):" % (mailbox.id))

	def addPVPResult(self,matchedPlayer,matchedChampion, player,playerChampion,player_match_number,match_order):#match_order ??match????????

		#?��match??????��????��
		#??????baseapp?????��match_order
		self.playerCal[player.id][match_order]=matchedPlayer

		#?????��????match?????????????????????????��????��???????
		if self.playerCal[player.id].__len__()==2:
			cal_result(player_match_number)

	#��?????????????	
	def cal_result(self,player_match_number):
		end_palyer=None
		
		min_val=30
		match_num=0 #��??????????��????baseapp
		for k ,v in self.playerCal[player.id].items():
			if v !=None:
				if min_val>abs(self.reqGetAttrs(v)-self.reqGetAttrs(player)):
					min_val=abs(self.reqGetAttrs(v)-self.reqGetAttrs(player))
					end_palyer=v
					match_num=k

		#???????��???????????????????????����???
		KBEngine.globalData["Rooms"].createSpace(0,{},self.playerCal[player.id][k], player)

		#?????????????��??��??��??��???????????
		#???????????��???��????????????

		del self.playerCal[player.id]
		del KBEngine.globalData["match1"%player_match_number].playerMatch[player.id]
		del KBEngine.globalData["match1"%k].playerMatch[end_palyer.id]

		#roomID=int(time.time()*100)

		#self.reqEnterRoom(self, roomID,self.playerMactch[player][x], player)

	#---------------------------------------------------------------------
	#                              Callbacks
	#---------------------------------------------------------------------
	def onTimer(self, tid, userArg):
		"""
		KBEngine method.
		???????��timer??��?
		"""
		#DEBUG_MSG("%s::onTimer: %i, tid:%i, arg:%i" % (self.getScriptName(), self.id, tid, userArg))
		
		GameObject.onTimer(self, tid, userArg)

	

