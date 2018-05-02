import sys, logging
from abc import ABCMeta, abstractmethod

class dev_type():
	NODE=1
	SWITCH=2
	ROUTER=3

class dev:
	__metaclass__ = ABCMeta
	# device id
	did=''
	# device type
	dtype=1

	def __init__(self, did=1, dtype=dev_type.NODE):
		pass

	def __str__(self):
		attrs = vars(self)
		return str(', '.join("%s: %s" % item for item in attrs.items()))

	@abstractmethod
	def uninstall(self):
		pass