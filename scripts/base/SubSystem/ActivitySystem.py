# -*- coding: utf-8 -*-
import KBEDebug
import py_util


class ActivitySystem:
	'''?ϵͳ'''
	def __init__(self):
		self.activityData=py_util._readXml('/data/xml/activityData.xml', 'id_i')
		self.missionData=py_util._readXml('/data/xml/activityData.xml', 'id_i')

	

	