import sys, logging
from abc import ABCMeta, abstractmethod

class node_type:
	SWITCH=0
	DEV=1
	ROUTER=2

class node:
	__metaclass__ = ABCMeta
	# device id
	did=''
	# device type
	dtype=1
	# device name
	name=''

	def __init__(self, did, name, dtype):
		self.did=did
		self.dtype=dtype
		self.name=name
		pass

	@abstractmethod
	def uninstall(self):
		pass