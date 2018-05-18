#!/usr/bin/env python
import XenAPI, logging, sys, subprocess
from sets import Set

sys.path.insert(0, '../utils')
sys.path.insert(0, './')

from node import node
from node import node_type
from helper import autolog as log

# TODO: how to set new bridge as none-automatically adding to new vms
class xswitch(node):
	# handle
	br=''

	def __init__(self, session, did, name):
		node.__init__(self, did, name, node_type.SWITCH)
		br_args={'bridge': name, 
				'assigned_ips': {}, 
				'name_label': name, 
				'name_description': '', 
				'MTU': '1500', 
				'other_config':{},
				'blobs': {}}
		self.br=session.xenapi.network.create(br_args)

	def plug(self, session, dev):
		return dev.create_vif_on_xbr(session, self)

	def uninstall(self, session):
		session.xenapi.network.destroy(self.br)
