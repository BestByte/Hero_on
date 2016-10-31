# -*- coding: utf-8 -*-
import KBEDebug
import py_util


class ActivitySystem:
	'''活动系统'''
	def __init__(self):
		self.activityData=py_util._readXml('/data/xml/activityData.xml', 'id_i')
		self.missionData=py_util._readXml('/data/xml/activityData.xml', 'id_i')

	

	