
# Flush and Reload

The FLUSH+RELOAD technique is a variant of PRIME+PROBE that relies on sharing pages between the spy and the victim processes. With shared pages, the spy can ensure that a specific memory line is evicted from the whole cache hierarchy. The spy uses this to monitor access to the memory line.           
A round of attack consists of three phases. During the first phase, the monitored memory line is flushed from the cache hierarchy. The spy, then, waits to allow the victim time to access the memory line before the third phase. In the third phase, the spy reloads the memory line, measuring the time to load it. If during the wait phase the victim accesses the memory line, the line will be available in the cache and the reload operation will take a short time. If, on the other hand, the victim has not accessed the memory line, the line will need to be brought from memory and the reload will take significantly longer. Figure 3 (A) and (B) show the timing of the attack phases without and with victim access. As shown in Fig. 3 (C), the victim access can overlap the reload phase of the spy. In such a case, the victim access will not trigger a cache fill. Instead, the victim will use the cached data from the reload phase. Consequently,
the spy will miss the access.                       
A similar scenario is when the reload operation partially overlaps the victim access. In this case, depicted in Fig. 3 (D), the reload phase starts while the victim is waiting for the data. The reload benefits from the victim access and terminates faster than if the data has to be loaded from memory. However, the timing may still be longer than a load from the cache. As the victim access is independent of the execution of the spy process code, increasing the wait period reduces the probability of missing the access due to an overlap. On the other hand, increasing the wait period reduces the granularity of the attack. One way to improve the resolution of the attack without increasing the error rate is to target memory accesses that occur frequently, such as a loop body. The attack will not be able to discern between separate accesses, but, as Fig. 3 (E) shows, the likelihood of missing the loop is small.                    
Several processor optimisations may result in false positives due to speculative memory accesses issued by the victim’s processor. These optimisations include data prefetching to exploit spatial locality and speculative execution. When analysing the attack results, the attacker must be aware of these optimisations and develop strategies to filter them.                           


<img align="center" src="https://github.com/Apurv3377/Cloud-Security-Project/blob/master/Unbenannt.PNG">

Task 1:Malware Detection using VMI with Volatility
--------------------

Tool Usage : 
vmidet one-xxxxx [-store <outputfile>]
vmidet one-xxxxx [-store <outputfile>] [-diff <inputfile>]

-store : creates the file with all the recorded information before attack
-diff : creates and detects the difference between previously created file

example : 
./vmidet.py one-23458 -store before
./vmidet.py one-23458 -store before -diff after


Attack:
mkdir /attack
mount 192.168.13.19:srv /attack
touch /attack/192.168.13.25

Information :
vmidet.py creates some internal file to comapre the VMI data with in-guest data.
For this comparison we have seperate tool "guest_comapre.py"

guest_compare Usage :
guest_compare [before/after]

before: This argument is to compare the VMI results before attack with commands (netstat -tap,ps aux,lsmod) executed on the wordpress/guest VM.
after: This argument is to compare the VMI results after attack with commands (netstat -tap, ps aux, lsmod) executed on the wordpress/guest VM.

example :
./guest_compare before
./guest_comapre after

Bonus Result Considerations:
pslist contains three extra PIDs always, they can be ignored as they are used for fetching the command outputs using python's paramiko.
netstat result is compared in terms of PIDs only, because the data from VMI(volatility) is different from the netstat -tap command.


TASK 2: Virtual machine manipulation with libvmi
-------------------------------------------------
For this project, we used volatility functions within a Python script. The first subtask was to initialize 
the address space and profile object. Then we got a reference to 'init_task' data structure and assigned it to a python object for convenience so that we could 
iterate over the tasks list. One of the user input was 'pid' which we used to match while iterating over the tasks list and once the match was found we copied a 
reference to the particular task object. Once the target task object was found the concerned elements were 'cred' and 'real_cred'. Since init_task's 'cred' and 
'real_cred' elements were pointing to the address of the credentials data structure which has root privilege we replaced the target task object's 'cred' and 
'real_cred' element to point to the address mentioned before. We did this using Libvmi passing it the target VM's name(which is the first user passed parameter) 
to get a handle and then replace the pointer with the above address.  We observed that the 'cred' and 'real_cred' elements point to the same address which is 
different for different tasks. But essentially, changing the pointer of 'real_cred' element make the process to change its privileges. We confirmed this by 
running 'ps aux | grep pid' command on PVM's console to see changes before and after running the script. Basic Input parameter checking is not mentioned in 
above explanation but implemented in the python script.

Usage : Assuming the uidchanger.py is in the directory named dir.
(One of the possible ways to run the script)
dir> python uidchanger.py "PVM-NAME" "PID"



Task 3 : System observation with system call tracing
----------------------------------------------------------

1. We are detecting a newly created ssh session and respective bash process using volatility. A list wiil be displayed with active sessions (if any)
2. we are calling "libvmitrace/csec" for tracing the system calls and interprocess communication between sshd and bash and 
   redirecting the same to a log file
3. we shall then filter the log file with desired ssh session and respective child bash process and moniter the interprocess 
   communication accordingly on seperate terminals activities can be monitored accordingly

The system call trace observation is documented in a separate pdf file - task 3.pdf   
