# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
from interfaces.GameObject import GameObject

import d_spaces

class Room(KBEngine.Entity, GameObject):
	"""
	??Ϸ????????????????Ұ??????ͼ
	"""
	def __init__(self):
		KBEngine.Entity.__init__(self)
		GameObject.__init__(self)
		
		# һ??space????????һ???????Ŀռ䣬???????????????Ŀռ??????˼?????Դ???ݣ???????????3D??????

		# ??space??ʹ??navigateѰ·ʹ?õ???3D??API????????2D?ļ???????navigateʹ?õ???astarѰ·
		resPath = d_spaces.datas.get(self.spaceUType)['resPath']
		#KBEngine.addSpaceGeometryMapping(self.spaceID, None, resPath, True, {0 : "srv_xinshoucun_1.navmesh", 1 : "srv_xinshoucun.navmesh"})

		#????Space????cell????֮???? cell?ϵ?Space._init__Ҳ?ᱻ???ã? ????addSpaceGeometryMapping API?ӿ????ɼ??????ݼ??ع???

		#??ע?⣺Ϊ?˼??ش??????ݲ??ý??̿??٣????????ݼ????Ƕ??̵߳ģ?????ͨ??һЩ?ص??????߿????߼???״̬???????ο?API?ֲᣩ??
		KBEngine.addSpaceGeometryMapping(self.spaceID, None, resPath)
		
		DEBUG_MSG('created space[%d] entityID = %i, res = %s.' % (self.spaceUType, self.id, resPath))
		
		KBEngine.globalData["space_%i" % self.spaceID] = self.base
	
	#--------------------------------------------------------------------------------------------
	#                              Callbacks
	#--------------------------------------------------------------------------------------------
	def onDestroy(self):
		"""
		KBEngine method.
		"""
		del KBEngine.globalData["space_%i" % self.spaceID]
		self.destroySpace()
		
	def onEnter(self, entityMailbox):
		"""
		defined method.
		???볡??
		"""
		DEBUG_MSG('Space::onEnter space[%d] entityID = %i.' % (self.spaceUType, entityMailbox.id))
		
	def onLeave(self, entityID):
		"""
		defined method.
		?뿪????
		"""
		DEBUG_MSG('Space::onLeave space[%d] entityID = %i.' % (self.spaceUType, entityID))
		
