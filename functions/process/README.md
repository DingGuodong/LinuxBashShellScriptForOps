# How to kill a process?
**some useful commands as follows:**
```
man 7 signal
kill -TERM $pid # SIGTERM 15
kill -KILL $pid # SIGKILL 9
kill -9 $pid # SIGKILL
ps -e -o ppid,stat | grep Z | cut -d” ” -f2 | xargs kill -9
kill -HUP `ps -A -ostat,ppid | grep -e ’^[Zz]‘ | awk ’{print $2}’`
kill -18 $pid # use SIGCONT/signal 18 to check if there are processes left.
cat /proc/[pid]/syscall
strace -p [pid]
ps -eo uname,pid,ppid,nlwp,pcpu,pmem,psr,start_time,tty,time,args --sort -pcpu,-pmem
ps -eo uname,pid,ppid,pcpu,pmem,args --sort -pcpu,-pmem
ps -eo uname,pid,ppid,pcpu,pmem,args --sort -pmem,-pcpu
ps -eo uname,pid,ppid,pcpu,pmem,args --sort -ppid
ps -a -uzabbix -o pid,ppid,stat,command
ps -eo pid,lstart,etime,args
lsof -p [pid]
lsof -i:[port]
```