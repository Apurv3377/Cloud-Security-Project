#!/usr/bin/env python
import sys
import os
import subprocess
from libvmi import Libvmi

def list_processes(vmi):
    tasksOffset = vmi.get_offset("linux_tasks")
    nameOffset = vmi.get_offset("linux_name")
    pidOffset = vmi.get_offset("linux_pid")
    init_task_va = vmi.translate_ksym2v("init_task")
    processes = vmi.read_addr_va(init_task_va+tasksOffset, 0)
    current_process = processes

    while True:
        pid = vmi.read_32_va(current_process+pidOffset-tasksOffset, 0)
        procname = vmi.read_str_va(current_process+nameOffset-tasksOffset, 0)

        yield pid, procname

        current_process = vmi.read_addr_va(current_process,0)

        if current_process == processes:
            break

    return



def list_other():
	network=os.popen("python /usr/src/volatility/vol.py --profile=LinuxDebian8x64 -f /mnt/mem linux_netstat -U").read()
	hidden_mods=os.popen("python /usr/src/volatility/vol.py --profile=LinuxDebian8x64 -f /mnt/mem linux_hidden_modules").read()
	loaded_mods=os.popen("python /usr/src/volatility/vol.py --profile=LinuxDebian8x64 -f /mnt/mem linux_lsmod").read()
	sp_network=os.popen("python /usr/src/volatility/vol.py --profile=LinuxDebian8x64 -f /mnt/mem linux_netstat -U | grep -o '[a-z0-9A-Z]*/[0-9]*' | awk -F'/' '{print $2}' | sort | uniq").read()
	sp_lsmod=os.popen("python /usr/src/volatility/vol.py --profile=LinuxDebian8x64 -f /mnt/mem linux_lsmod | awk '{print $2" "$3}'").read()
	return (network,hidden_mods,loaded_mods,sp_network,sp_lsmod)


if (len(sys.argv)==4):
        vmi = Libvmi(sys.argv[1])
        f=open(sys.argv[3],'w')
	f1=open("net_be",'w')
	f2=open("lsmod_be","w")
	f3=open("pslist_be","w")

	for pid, procname in list_processes(vmi):
		f.write("%s %s\n" % (pid, procname))
		f3.write("%s %s\n" % (pid, procname))
	(network,hidden_mods,loaded_mods,sp_network,sp_lsmod)=list_other()
	f.write("\n%s\n" % network)
	f.write("%s\n" % hidden_mods)
	f.write("%s" % loaded_mods)
	f1.write("%s" % sp_network)
	f2.write("%s" % sp_lsmod)

        f.close()
	f1.close()
	f2.close()
	f3.close()
	exit()
elif (len(sys.argv)==6):
        vmi = Libvmi(sys.argv[1])
        f=open(sys.argv[5],'w')
	f1=open("net_af",'w')
	f2=open("lsmod_af","w")
        f3=open("pslist_af","w")

        for pid, procname in list_processes(vmi):
                f.write("%s, %s\n" % (pid, procname))
		f3.write("%s %s\n" % (pid, procname))
        (network,hidden_mods,loaded_mods,sp_network,sp_lsmod)=list_other()
        f.write("\n%s\n" % network)
        f.write("%s\n" % hidden_mods)
        f.write("%s" % loaded_mods)
	f1.write("%s" % sp_network)
        f2.write("%s" % sp_lsmod)

        f.close()
	f1.close()
	f2.close()
        f3.close()

	before=sys.argv[3]
	after=sys.argv[5]
	subprocess.Popen(["diff","-y",before,after])
	exit()
else:
        print "USAGE : vmidet one-xxxxx [-store <outputfile>]"
        print "USAGE : vmidet one-xxxxx [-store <outputfile>] [-diff <inputfile>]"
	exit()

