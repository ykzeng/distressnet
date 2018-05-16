import os
import subprocess
import logging, sys
import XenAPI

sys.path.insert(0, './bean')
sys.path.insert(0, './utils')

from vm import vm
from dev import dev
from helper import initializer
from helper import autolog as log
from xswitch import xswitch

class xen_net:
	def __init__(self, uname, pwd, template_lst):
		# a list of 'dev' instances
		self.dev_list=[]
		# a dict that stores <name, template_ref(vm_ref)> pairs
		self.template_dict={}
		self.emp_ids=[0]
		self.session=xen_net.init_session(uname, pwd)
		self.init_templates(template_lst)
		# init a dummy bridge
		self.create_new_xbr('dummy')
		pass

	@staticmethod
	def init_session(uname, pwd):
		session=XenAPI.xapi_local()
		session.xenapi.login_with_password(uname, pwd)
		return session

	def init_templates(self, tname_arr):
		for tname in tname_arr:
			lst=self.session.xenapi.VM.get_by_name_label(tname)
			count=len(lst)
			if count==1:
				self.template_dict[tname]=lst[0]
				continue
			elif(count<1):
				msg="too less templates (" + str(count) + ") found for " + tname
			else:
				msg="too many templates (" + str(count) + ") found for " + tname
			log(msg)

	# ATTENTION: when no empty slot is found, open a new slot for the new id, which need
	# to be used immediately
	def get_new_id(self):
		if len(self.emp_ids)==1:
			did=self.emp_ids[0]
			self.dev_list.append(None)
			self.emp_ids[0]+=1
			return did
		else:
			last=len(self.emp_ids)-1
			did=self.emp_ids[last]
			self.emp_ids=self.emp_ids[:-1]

	def del_node(self, did):
		self.dev_list[did].uninstall()
		self.emp_ids.append(did)

	def get_node(self, did):
		return self.dev_list[did]

	def create_new_node(self, tname, name, override, vcpu=0, mem=0):
		did=self.get_new_id()
		template=self.template_dict[tname]
		node=vm(self.session, did, template, name)
		if override:
			node.set_fixed_VCPUs(self.session, vcpu)
			node.set_memory(self.session, mem)
		self.dev_list[did]=node
		return node

	def create_new_xbr(self, name):
		did=self.get_new_id()
		br=xswitch(self.session, did, name)
		self.dev_list[did]=br
		return br

	def clear(self):
		for i in range(0, len(self.dev_list)):
			if i not in self.emp_ids:
				self.dev_list[i].uninstall(self.session)
		self.dev_list=[]
		self.emp_ids=[0]

	def start_node(self, did):
		node=self.dev_list[did]
		node.start(self.session)

	def shutdown_node(self, did):
		node=self.dev_list[did]
		node.shutdown(self.session)

	# start all nodes
	# ATTENTION: we may need to start router/switch first here
	# if they are involved in the future
	def start_all(self):
		for dev in self.dev_list:
			dev.start(self.session)

class net_graph:
	test=None


class link_prop:
	# 
	delay=10

def test_main():
	# simple logging
	#FORMAT = "[%(levelname)s - %(filename)s:%(lineno)s - %(funcName)s() ] %(message)s"
	logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
	# init xennet with templates we would like to use
	tlst=['android-basic', 'android-terminal']
	xnet=xen_net("root", "789456123", tlst)
	# creating test nodes
	test1=xnet.create_new_node('android-basic', 'py_test1', override=True, vcpu=4, mem=str(2048*1024*1024))
	test2=xnet.create_new_node('android-terminal', 'py_test2', override=False)
	return xnet