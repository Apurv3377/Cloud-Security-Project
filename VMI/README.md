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


