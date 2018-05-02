import os
import subprocess
import logging, sys

sys.path.insert(0, './bean')
sys.path.insert(0, './utils')

from vm import vm
from dev import dev
from helper import initializer

class xen_net:
	def __init__(self):
		self.dev_list=[]
		self.emp_ids=[0]
		pass

	def get_new_id(self):
		if len(self.emp_ids)==1:
			did=self.emp_ids[0]
			self.emp_ids[0]+=1
			return did
		else:
			last=len(self.emp_ids)-1
			did=self.emp_ids[last]
			self.emp_ids=self.emp_ids[:-1]

	def del_node(self, id):
		self.dev_list[id].uninstall()
		self.dev_list[id]=None
		self.emp_ids.append(id)

	def get_new_node(self, tid, name, override, vcpu=0, mem=0):
		did=self.get_new_id()
		nvm=vm(did, tid, name, override, vcpu, mem)
		if did >= len(self.dev_list):
			self.dev_list.append(nvm)
		else:
			self.dev_list[did]=nvm
		return nvm

	def clear(self):
		for dev in self.dev_list:
			if dev!=None:
				dev.uninstall()
		self.dev_list=[]
		self.emp_ids=[0]

class net_graph:
	test=None

class link_prop:
	# 
	delay=10

def test_main():
	# test the get snapshot id method
	#print get_snapshot_id("mcloud v0.3")
	#print get_snapshot_id("lalalalala")
	#vm_obj=vm(1, vm_type.NODE, 123, 123, 1, 1024)
	#print "vm_obj"
	#print vm_obj
	#dev_obj=dev(1, vm_type.NODE)
	#print "dev_obj"
	#print dev_obj
	FORMAT = "[%(levelname)s - %(filename)s:%(lineno)s - %(funcName)s() ] %(message)s"
	logging.basicConfig(stream=sys.stderr, level=logging.DEBUG, format=FORMAT)
	#test_vm1=vm(1, '24d531ee-35bc-b072-eb55-73c7e9569e38', 'py_test1', override=True, vcpu=4, mem=2048)
	#test_vm2=vm(2, '24d531ee-35bc-b072-eb55-73c7e9569e38', 'py_test2', override=False)
	xnet=xen_net()
	test1=xnet.get_new_node('24d531ee-35bc-b072-eb55-73c7e9569e38', 'py_test1', override=True, vcpu=4, mem=2048)
	test2=xnet.get_new_node('24d531ee-35bc-b072-eb55-73c7e9569e38', 'py_test2', override=False)
	return xnet