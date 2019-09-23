#!/usr/bin/env python
import paramiko
import sys
import subprocess


def cmd_exe():
    ip = '192.168.13.25'
    port = 22
    username = 'root'
    password = 'password'
    cmd = "ps axo pid,comm | grep -v 'PID COMMAND'"
    cmd1 = "lsmod | awk '{print $1" "$2}'| grep -v Module"
    cmd2="netstat -tap |awk '{print $7}'| grep -v Address | awk -F'/' '{print $1}'| awk '{if(NR>1)print}' | sort | uniq"
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, port, username, password)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    outlines = stdout.readlines()
    resp1 = ''.join(outlines)

    stdin, stdout, stderr = ssh.exec_command(cmd2)
    outlines = stdout.readlines()
    resp2 = ''.join(outlines)

    stdin, stdout, stderr = ssh.exec_command(cmd1)
    outlines = stdout.readlines()
    resp3 = ''.join(outlines)
    return (resp1, resp2, resp3)


def file_gen():
	f0 = open(sys.argv[1] + "_pslist", 'w')
	f2 = open(sys.argv[1] + "_lsmod", 'w')
	f3 = open(sys.argv[1] + "_net", 'w')
	(resp1, resp2, resp3) = cmd_exe()
	f0.write("%s" % resp1)
	f3.write("%s" % resp2)
	f2.write("%s" % resp3)
	f0.close()
	f2.close()
	f3.close()
	return 0

if (len(sys.argv)==1):
    print "Usage: guest_compare [before/after]"
    exit()
if (len(sys.argv)>2):
   print "Usage: guest_compare [before/after]"
   exit()

if (sys.argv[1] == "before"):
    file_gen()
    print "GUEST Stats                                                VMI Stats"
    subprocess.Popen(["echo", "-------------------------\"ps aux\"-------------------------------------------"])
    subprocess.Popen(["diff", "-y", sys.argv[1]+"_pslist", "pslist_be"])
    subprocess.Popen(["echo", "-------------------------\"netstat PIDs\"-------------------------------------"])
    subprocess.Popen(["diff", "-y",sys.argv[1]+"_net", "net_be"])
    subprocess.Popen(["echo", "-------------------------\"lsmod\"--------------------------------------------"])
    subprocess.Popen(["diff", "-y",sys.argv[1]+"_lsmod", "lsmod_be"])
    
if (sys.argv[1] == "after"):
    file_gen()
    print "GUEST Stats                                                VMI Stats"
    subprocess.Popen(["echo", "-------------------------\"ps aux\"-------------------------------------------"])
    subprocess.Popen(["diff", "-y", sys.argv[1]+"_pslist", "pslist_af"])
    subprocess.Popen(["echo", "-------------------------\"netstat PIDs\"-------------------------------------"])
    subprocess.Popen(["diff", "-y",sys.argv[1]+"_net", "net_af"])
    subprocess.Popen(["echo", "-------------------------\"lsmod\"--------------------------------------------"])
    subprocess.Popen(["diff", "-y",sys.argv[1]+"_lsmod", "lsmod_af"])

