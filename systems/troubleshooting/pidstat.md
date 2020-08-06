# pidstat

Report statistics for Linux tasks.

## Synopsis

```
pidstat [ -d ] [ -H ] [ -h ] [ -I ] [ -l ] [ -R ] [ -r ] [ -s ] [ -t ] [ -U [ username ] ] [ -u ] [ -V ] [ -v ] [ -w ] [ -C comm ] [ -G process_name ] [ --dec={ 0 | 1 | 2 } ] [ --human ] [ -p { pid [,...] | SELF | ALL } ] [ -T { TASK | CHILD | ALL } ] [ interval [ count ] ] [ -e program args ]
```

## Description

The **pidstat** command is used for monitoring individual tasks currently being managed by the Linux kernel.
It writes to standard output activities for every task selected with option **-p** or for every task managed by the Linux kernel if option -p ALL has been used.
Not selecting any tasks is equivalent to specifying -p ALL but only active tasks (tasks with non-zero statistics values) will appear in the report.

The **pidstat** command can also be used for monitoring the child processes of selected tasks.
Read about option **-T** below.

The interval parameter specifies the amount of time in seconds between each report.
A value of 0 (or no parameters at all) indicates that tasks statistics are to be reported for the time since system startup (boot).
The count parameter can be specified in conjunction with the interval parameter if this one is not set to zero.
The value of count determines the number of reports generated at interval seconds apart.
If the interval parameter is specified without the count parameter, the **pidstat** command generates reports continuously.

You can select information about specific task activities using flags.
Not specifying any flags selects only CPU activity.

## Options

-t     Also display statistics for threads associated with selected tasks.

This option adds the following values to the reports:

**TGID**
      The identification number of the thread group leader.

**TID**
      The identification number of the thread being monitored.

-u     Report CPU utilization.

       When reporting statistics for individual tasks, the following values may be displayed:

-w     Report task switching activity (kernels 2.6.23 and later only).
The following values may be displayed:

UID
     The real user identification number of the task being monitored.

USER
     The name of the real user owning the task being monitored.

PID
     The identification number of the task being monitored.

cswch/s
     Total number of voluntary context switches the task made per second.  A voluntary context switch occurs when a task blocks because it requires a resource that is unavailable.

nvcswch/s
     Total  number  of  non voluntary context switches the task made per second.  A involuntary context switch takes place when a task executes for the duration of its time slice and
     then is forced to relinquish the processor.

Command
     The command name of the task.
