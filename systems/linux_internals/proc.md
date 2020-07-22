# proc

process information pseudo-filesystem

## Description

### Mount Options

### Files and directories

The following list describes many of the files and directories under the /proc hierarchy.
```
/proc/[pid]
```
There is a numerical subdirectory for each running process;
the subdirectory is named by the process ID.

```
/proc/cpuinfo
```
This is a collection of CPU and system architecture dependent items, for each supported architecture a different list.
Two common entries are processor which gives CPU number and bogomips;
a system constant that is calculated during kernel initialization.
SMP machines have information for each CPU.
The lscpu(1) command gathers its information from this file.

```
/proc/interrupts
```
This is used to record the number of interrupts per CPU per IO device.
Since Linux 2.6.24, for the i386 and x86-64 architectures, at least, this also includes interrupts internal to the system (that is, not associated with a device as such), such as NMI (nonmaskable interrupt), LOC (local timer interrupt), and for SMP systems, TLB (TLB flush interrupt), RES (rescheduling interrupt), CAL (remote function call interrupt), and possibly others.
Very easy to read formatting, done in ASCII.

```
/proc/loadavg
```

```
/proc/meminfo
```

```
/proc/sys/kernel/sysrq
```

```
/proc/uptime
```

```
/proc/version
```
