#!/usr/bin/env python


import sys
sys.path.append("/usr/src/volatility")
origargv = sys.argv
#sys.argv = [sys.argv[0], "-f", "/mnt/mem", "--profile", "LinuxDebian8x64"]
#sys.argv=[]
import os
import socket
import time
import volatility.conf as conf
import volatility.utils as utils
import volatility.obj as obj
import volatility.addrspace as addrspace
import volatility.registry as registry

from libvmi import Libvmi

# Global vars
vmi=None
vm_name=""
p_id=""
#p=None
a=None
i=None
init_task_addr=""


def init_config():
    sys.path.append("/usr/src/volatility")
    origargv = sys.argv
    sys.argv = [sys.argv[0], "-f", "/mnt/mem", "--profile", "LinuxDebian8x64"]

    config = conf.ConfObject()
    registry.PluginImporter()
    registry.register_global_options(config, addrspace.BaseAddressSpace)

    # Initialize address space (same as a=addrspace() in linux_volshell)
    global a
    a=utils.load_as(config)
    global p
    p=a.profile
    print("in init.. p = ",p) 
    # Lookup kernel symbol pointing to first module
    global init_task_addr 
    i = p.get_symbol("init_task")
    init = obj.Object("task_struct", vm=a, offset=i)

def change_uid_process(vmi, p_id):
    global p
    global a
    print("in change_uid.. p = ",p)
    i = p.get_symbol("init_task")
    init = obj.Object("task_struct", vm=a, offset=i)
    #print init.pid, init.comm.v()
    print "Alles Gute"

    l=list(init.tasks)
    apach_proc = init
    for t in l:
	#print("t.pid = ",t.pid, " p_id = ",p_id)
        if t.pid==int(p_id):
                apach_proc=t
                print "found again"
                break;

    apach_proc_va = apach_proc.cred.obj_offset
    apach_proc_pa = a.vtop(apach_proc_va)
    apach_proc_real_va = apach_proc.real_cred.obj_offset
    apach_proc_real_pa = a.vtop(apach_proc_real_va)

    #vmi = Libvmi("one-23458")
    vmi.write_64_pa(apach_proc_pa,init.cred)
    vmi.write_64_pa(apach_proc_real_pa,init.cred)	
    return True

def main(args):
    if len(args) != 3:
        print('Incorrect number of args', args)
	print('arg 2', args[1])
        return
    init_config()
    vm_name = args[1]
    p_id = args[2]
    print('Received : vm_name = '+vm_name+' , p_id = '+p_id)
    vmi = Libvmi(vm_name)
    result = change_uid_process(vmi, p_id)
    if result:
        print("uid changed successfully!")
    else:
        print("something went wrong!")


if __name__ == '__main__':
    main(sys.argv)
