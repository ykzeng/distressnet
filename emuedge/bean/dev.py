import sys, logging
from node import node
from node import node_type
from abc import abstractmethod

class dev(node):

	def __init__(self, did=1, dtype=node_type.NODE):
		node.__init__(did, dtype)
		pass

	def __str__(self):
		attrs = vars(self)
		return str(', '.join("%s: %s" % item for item in attrs.items()))

	@abstractmethod
	def start(self, session=None):
		pass

	@abstractmethod
	def shutdown(self, session=None):
		pass