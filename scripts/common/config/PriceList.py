import py_util
from KBEDebug import *
class PriceList:
	#管理物品价格列表
	def __init__(self):
		cfgData = py_util._readXml("/data/xml/PriceList.xml", "id_i")
		self.cfgData = cfgData
		for _,v in self.cfgData.items():
			self.VerifyData(v)

	def VerifyData(self,itemData):
		pass
	#--获取对应类型物品的价格定义
	#--id表示表中物品的索引值
	def GetPriceData(self,idx):
		if self.cfgData:
			return self.cfgData[idx]