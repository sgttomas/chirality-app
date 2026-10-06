#include <libproc.h>
#include <sys/proc_info.h>
#include <unistd.h>
#include <stdio.h>
#include <stdint.h>
uint64_t peer(int fd){struct pipe_fdinfo info;int n=proc_pidfdinfo(getpid(),fd,PROC_PIDFDPIPEINFO,&info,sizeof(info));return n==sizeof(info)?info.pipeinfo.pipe_peerhandle:0;}
int reader(int pid,uint64_t target){for(int fd=0;fd<256;fd++){struct pipe_fdinfo info;int n=proc_pidfdinfo(pid,fd,PROC_PIDFDPIPEINFO,&info,sizeof(info));if(n==sizeof(info)&&info.pipeinfo.pipe_handle==target){fprintf(stderr,"MATCH reader_pid=%d fd=%d flags=%u status=%u handle=%llx peer=%llx\n",pid,fd,info.pfi.fi_openflags,info.pfi.fi_status,info.pipeinfo.pipe_handle,info.pipeinfo.pipe_peerhandle);return fd+1;}}return 0;}
int childreader(uint64_t target){int pids[512];int count=proc_listchildpids(getpid(),pids,sizeof(pids))/sizeof(int);for(int j=0;j<count;j++){if(pids[j]>0&&reader(pids[j],target)>0)return pids[j];}return 0;}
