#!/usr/bin/env python
import os


# getting a list of ssh and bash process

os.popen("python /usr/src/volatility/vol.py --profile=LinuxDebian8x64 -f /mnt/mem linux_netstat -U |grep 'ESTABLISHED.*sshd' |cut -d'/' -f2  > sshdlist.txt")
os.popen("python /usr/src/volatility/vol.py --profile=LinuxDebian8x64 -f /mnt/mem linux_pstree | grep bash | awk '{print $2}'  > bashlist.txt")

sshd_list = []
bash_list = []

# reading from a list of ssh sessions  and storing it in a Python List

with open("sshdlist.txt", "r") as sshfile:
    for line in sshfile:
        sshd_list.append(line)

# reading from a list of bash process list and storing in a Python list

with open("bashlist.txt", "r") as bashfile:
    for bashline in bashfile:
        bash_list.append(bashline)


if not sshd_list:
    print("\nCurrently there is NO active SSH session !!!")

# if active ssh session is detected 

else:
   print(".....sshd process list...")
   print(sshd_list)
   print("....bash process list....")
   print (bash_list)
   print("\ncreating a log for active sessions... ..")

# creating a log of system calls and interprocess communication

   cmd_Log = "/root/libvmtrace2/apps/csec one-23458 > /root/task_3/vmComm.log"
   os.system(cmd_Log)




