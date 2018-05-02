import sys, logging, subprocess

sys.path.insert(0, './')
sys.path.insert(0, '../utils/')

from xen_helper import xen_helper
from dev import dev
from dev import dev_type

class vm(dev):
	# snapshot id
	#ssid=''
	# template id
	#tid=''
	
	# vcpu cores
	vcpu=1
	# memory in MB
	mem=1024
	# vm id
	vid=1
	# vm name label
	vname=''
	# vm device type
	dtype=dev_type.NODE
	# snapshot or tempalteid the vm based on
	ssid=''

	def __init__(self, did, ssid, vname, override=True, vcpu=1, mem=1024):
		dev.__init__(self, did)
		self.did=did
		self.ssid=ssid
		self.vname=vname
		if override:
			self.vcpu=vcpu
			self.mem=mem
		self.install(ssid, override, 'snapshot')
		pass

	# install the vm based on snapshot/template ssid
	# by default this create vm by snapshot
	def install(self, ssid, override=True, opt='snapshot'):
		if opt=='snapshot':
			cmd=("xe vm-install new-name-label=" + self.vname + " template=" + self.ssid)
			self.vid=subprocess.check_output(cmd, shell=True).rstrip()
			logging.debug(self.vid)
			if override:
				cmd=("xe vm-param-set uuid=" + self.vid + " VCPUs-max=" + str(self.vcpu) + " VCPUs-at-startup=" + str(self.vcpu))
				logging.debug(cmd)
				subprocess.call(cmd, shell=True)

				cmd=("xe vm-memory-set vm=" + self.vid + " memory=" + str(self.mem) + "MiB")
				logging.debug(cmd)
				subprocess.call(cmd, shell=True)
			else:
				self.vcpu=xen_helper.get_vm_param(self.vid, "VCPUs-number")
				self.mem=xen_helper.get_vm_param(self.vid, "memory-actual")
		else:
			print "unrecognized template to boot from"
		pass

	def start(self):
		cmd=("xe vm-start uuid=" + self.vid)
		subprocess.call(cmd, shell=True)
		pass

	def shutdown(self):
		cmd=("xe vm-shutdown uuid=" + self.vid)
		msg=subprocess.call(cmd, shell=True)
		return msg

	def f_shutdown(self):
		cmd=("xe vm-shutdown --force uuid=" + self.vid)
		msg=subprocess.call(cmd, shell=True)
		return msg

	def uninstall(self):
		cmd=("xe vm-uninstall --force uuid=" + self.vid)
		msg=subprocess.call(cmd, shell=True)
		return msg