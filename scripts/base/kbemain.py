# -*- coding: utf-8 -*-
import KBEngine
import Watcher
import d_spaces
import items
from KBEDebug import *
import os
import  math
global ser_number 
import re

def onBaseAppReady(isBootstrap):
	"""
	KBEngine method.
	baseapp已经准备好了
	@param isBootstrap: 是否为第一个启动的baseapp
	@type isBootstrap: BOOL
	"""
	INFO_MSG('onBaseAppReady: isBootstrap=%s' % isBootstrap)
	
	# 安装监视器
	Watcher.setup()
	
	ser_number= int(os.getenv("KBE_BOOTIDX_GROUP"))
	INFO_MSG('onBaseAppReady: ser_number=%s' % ser_number)

	#不论第几个baseAPP，都要创建匹配实体Match
	if isBootstrap:
		# 创建spacemanager
		KBEngine.createBaseLocally( "Match", {} )
		KBEngine.setAppFlags(KBEngine.APP_FLAGS_NOT_PARTCIPATING_LOAD_BALANCING )
		
	elif int(os.getenv("KBE_BOOTIDX_GROUP"))==2 :
		KBEngine.createBaseLocally( "Match", {} )
		KBEngine.setAppFlags(KBEngine.APP_FLAGS_NOT_PARTCIPATING_LOAD_BALANCING )

	elif int(os.getenv("KBE_BOOTIDX_GROUP"))==3 :
		KBEngine.createBaseLocally( "Rooms", {} )


def onBaseAppShutDown(state):
	"""
	KBEngine method.
	这个baseapp被关闭前的回调函数
	@param state:  0 : 在断开所有客户端之前
						 1 : 在将所有entity写入数据库之前
						 2 : 所有entity被写入数据库之后
	@type state: int					 
	"""
	INFO_MSG('onBaseAppShutDown: state=%i' % state)
	
def onReadyForLogin(isBootstrap):
	"""
	KBEngine method.
	如果返回值大于等于1.0则初始化全部完成, 否则返回准备的进度值0.0~1.0。
	在此可以确保脚本层全部初始化完成之后才开放登录。
	@param isBootstrap: 是否为第一个启动的baseapp
	@type isBootstrap: BOOL
	"""
	if not isBootstrap:
		INFO_MSG('initProgress: completed!')
		return 1.0
		
	INFO_MSG('initProgress: completed!')
	return 1.0

def onAutoLoadEntityCreate(entityType, dbid):
	"""
	KBEngine method.
	自动加载的entity创建方法，引擎允许脚本层重新实现实体的创建，如果脚本不实现这个方法
	引擎底层使用createBaseAnywhereFromDBID来创建实体
	"""
	INFO_MSG('onAutoLoadEntityCreate: entityType=%s, dbid=%i' % (entityType, dbid))
	KBEngine.createBaseAnywhereFromDBID(entityType, dbid)
	
def onInit(isReload):
	"""
	KBEngine method.
	当引擎启动后初始化完所有的脚本后这个接口被调用
	@param isReload: 是否是被重写加载脚本后触发的
	@type isReload: bool
	"""
	INFO_MSG('onInit::isReload:%s' % isReload)

def onFini():
	"""
	KBEngine method.
	引擎正式关闭
	"""
	INFO_MSG('onFini()')
	
def onCellAppDeath(addr):
	"""
	KBEngine method.
	某个cellapp死亡
	"""
	WARNING_MSG('onCellAppDeath: %s' % (str(addr)))
	
def onGlobalData(key, value):
	"""
	KBEngine method.
	globalData有改变
	"""
	DEBUG_MSG('onGlobalData: %s' % key)
	
def onGlobalDataDel(key):
	"""
	KBEngine method.
	globalData有删除
	"""
	DEBUG_MSG('onDelGlobalData: %s' % key)

def onBaseAppData(key, value):
	"""
	KBEngine method.
	baseAppData有改变
	"""
	DEBUG_MSG('onBaseAppData: %s' % key)
	
def onBaseAppDataDel(key):
	"""
	KBEngine method.
	baseAppData有删除
	"""
	DEBUG_MSG('onBaseAppDataDel: %s' % key)

def onLoseChargeCB(ordersID, dbid, success, datas):
	"""
	KBEngine method.
	有一个不明订单被处理， 可能是超时导致记录被billing
	清除， 而又收到第三方充值的处理回调
	"""
	DEBUG_MSG('onLoseChargeCB: ordersID=%s, dbid=%i, success=%i, datas=%s' % \
							(ordersID, dbid, success, datas))


