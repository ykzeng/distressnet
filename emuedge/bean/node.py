import sys, logging
from abc import ABCMeta, abstractmethod

class node_type:
	NODE=1
	SWITCH=2
	ROUTER=3
	SHELL=4

class node:
	__metaclass__ = ABCMeta
	# device id
	did=''
	# device type
	dtype=1

	def __init__(self, did=1, dtype=node_type.NODE):
		self.did=did
		self.dtype=dtype
		pass

	@abstractmethod
	def uninstall(self):
		pass