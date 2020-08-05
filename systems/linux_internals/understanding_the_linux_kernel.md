# Understanding the Linux Kernel, 3rd Edition

## Chapter 1 Introduction

Linux was initially developed by Linus Torvalds in 1991 as an operating system for IBM-compatible personal computers based on the Intel 80386 microprocessor.

Technically speaking, Linux is a true Unix kernel, although it is not a full Unix operating system because it does not include all the Unix applications, such as filesystem utilities, windowing systems and    graphical desktops, system administrator commands, text editors, compilers, and so on.

### Linux Versus Other Unix-Like Kernels

To define a common user interface, Unix-like kernels often share fundamental design ideas and features.
In this respect, Linux is comparable with the other Unix-like operating systems.

### Hardware Dependency

Linux tries to maintain a neat distinction between hardware-dependent and hardware-independent source code.
To that end, both the arch and the include directories include 23 subdirectories that correspond to the different types of hardware platforms supported.

### Linux Versions

Please be aware that the kernel version described in this book is Linux 2.6.11.

### Basic Operating System Concepts

The operating system must fulfill two main objectives:
* Interact with the hardware components, servicing all low-level programmable elements included in the hardware platform.
* Provide an execution environment to the applications that run on the computer system (the so-called user programs).

Some operating systems allow all user programs to directly play with the hardware components (a typical example is MS-DOS).
In contrast, a Unix-like operating system hides all low-level details concerning the physical organization of the computer from applications run by the user.
When a program wants to use a hardware resource, it must issue a request to the operating system.
The kernel evaluates the request and, if it chooses to grant the resource, interacts with the proper hardware components on behalf of the user program.

To enforce this mechanism, modern operating systems rely on the availability of specific hardware features that forbid user programs to directly interact with low-level hardware components or to access arbitrary memory locations.
In particular, the hardware introduces at least two different *execution modes* for the CPU: a nonprivileged mode for user programs and a privileged mode for the kernel.
Unix calls these *User Mode* and *Kernel Mode*, respectively.

#### Multiuser Systems

A *multiuser system* is a computer that is able to concurrently and independently execute several applications belonging to two or more users.
*Concurrently* means that applications can be active at the same time and contend for the various resources such as CPU, memory, hard disks, and so on.
*Independently* means that each application can perform its task with no concern for what the applications of the other users are doing.
Switching from one application to another, of course, slows down each of them and affects the response time seen by the users.
Many of the complexities of modern operating system kernels, which we will examine in this book, are present to minimize the delays enforced on each program and to provide the user with responses that are as fast as possible.

Multiuser operating systems must include several features:
* An authentication mechanism for verifying the user's identity
* A protection mechanism against buggy user programs that could block other applications running in the system
* A protection mechanism against malicious user programs that could interfere with or spy on the activity of other users
* An accounting mechanism that limits the amount of resource units assigned to each user

To ensure safe protection mechanisms, operating systems must use the hardware protection associated with the CPU privileged mode.
Otherwise, a user program would be able to directly access the system circuitry and overcome the imposed bounds.
Unix is a multiuser system that enforces the hardware protection of system resources.

#### Users and Groups

#### Processes

All operating systems use one fundamental abstraction: the *process*.
A process can be defined either as "an instance of a program in execution" or as the "execution context" of a running program.
In traditional operating systems, a process executes a single sequence of instructions in an address space;
the address space is the set of memory addresses that the process is allowed to reference.
Modern operating systems allow processes with multiple execution flows — that is, multiple sequences of instructions executed in the same address space.

Multiuser systems must enforce an execution environment in which several processes can be active concurrently and contend for system resources, mainly the CPU.
Systems that allow concurrent active processes are said to be *multiprogramming* or *multiprocessing*.

On uniprocessor systems, just one process can hold the CPU, and hence just one execution flow can progress at a time.
In general, the number of CPUs is always restricted, and therefore only a few processes can progress at once.
An operating system component called the *scheduler* chooses the process that can progress.
Some operating systems allow only *nonpreemptable* processes, which means that the scheduler is invoked only when a process voluntarily relinquishes the CPU.
But processes of a multiuser system must be preemptable;
the operating system tracks how long each process holds the CPU and periodically activates the scheduler.

Unix is a multiprocessing operating system with preemptable processes.
Even when no user is logged in and no application is running, several system processes monitor the peripheral devices.
In particular, several processes listen at the system terminals waiting for user logins.
When a user inputs a login name, the listening process runs a program that validates the user password.
If the user identity is acknowledged, the process creates another process that runs a shell into which commands are entered.
When a graphical display is activated, one process runs the window manager, and each window on the display is usually run by a separate process.
When a user creates a graphics shell, one process runs the graphics windows and a second process runs the shell into which the user can enter the commands.
For each user command, the shell process creates another process that executes the corresponding program.

### An Overview of the Unix Filesystem

#### Files

#### Hard and Soft Links

To overcome these limitations, *soft links* (also called *symbolic links*) were introduced a long time ago.
Symbolic links are short files that contain an arbitrary pathname of another file.
The pathname may refer to any file or directory located in any filesystem;
it may even refer to a nonexistent file.

#### File Types

#### File Descriptor and inode

Unix makes a clear distinction between the contents of a file and the information about a file.
With the exception of device files and files of special filesystems, each file consists of a sequence of bytes.
The file does not include any control information, such as its length or an end-of-file (EOF) delimiter.

All information needed by the filesystem to handle a file is included in a data structure called an *inode*.
Each file has its own inode, which the filesystem uses to identify the file.

#### File-Handling System Calls

### An Overview of Unix Kernels

Unix kernels provide an execution environment in which applications may run.
Therefore, the kernel must implement a set of services and corresponding interfaces.
Applications use those interfaces and do not usually interact directly with hardware resources.

#### The Process/Kernel Model

#### Process Implementation

To let the kernel manage processes, each process is represented by a *process descriptor* that includes information about the current state of the process.

When the kernel stops the execution of a process, it saves the current contents of several processor registers in the process descriptor.

When the kernel decides to resume executing a process, it uses the proper process descriptor fields to load the CPU registers.
Because the stored value of the program counter points to the instruction following the last instruction executed, the process resumes execution at the point where it was stopped.

#### Reentrant Kernel

All Unix kernels are *reentrant*.
This means that several processes may be executing in Kernel Mode at the same time.
Of course, on uniprocessor systems, only one process can progress, but many can be blocked in Kernel Mode when waiting for the CPU or the completion of some I/O operation.

#### Process Address Space

Each process runs in its private address space.
A process running in User Mode refers to private stack, data, and code areas.
When running in Kernel Mode, the process addresses the kernel data and code areas and uses another private stack.

#### Synchronization and Critical Regions

#### Signals and IPC

Unix *signals* provide a mechanism for notifying processes of system events.
Each event has its own signal number, which is usually referred to by a symbolic constant such as `SIGTERM`.
There are two kinds of system events:
* Asynchronous notifications
* Synchronous notifications

The POSIX standard defines about 20 different signals, 2 of which are user-definable and may be used as a primitive mechanism for communication and synchronization among processes in User Mode.
In general, a process may react to a signal delivery in two possible ways:
* Ignore the signal.
* Asynchronously execute a specified procedure (the signal handler).

If the process does not specify one of these alternatives, the kernel performs a default action that depends on the signal number.
The five possible default actions are:
* Terminate the process.
* Write the execution context and the contents of the address space in a file (core dump) and terminate the process.
* Ignore the signal.
* Suspend the process.
* Resume the process's execution, if it was stopped.

Kernel signal handling is rather elaborate, because the POSIX semantics allows processes to temporarily block signals.
Moreover, the SIGKILL and SIGSTOP signals cannot be directly handled by the process or ignored.

#### Process Management

#### Memory Management

##### Virtual Memory

All recent Unix systems provide a useful abstraction called *virtual memory*.
Virtual memory acts as a logical layer between the application memory requests and the hardware Memory Management Unit (MMU).
Virtual memory has many purposes and advantages:
* Several processes can be executed concurrently.
* It is possible to run applications whose memory needs are larger than the available physical memory.
* Processes can execute a program whose code is only partially loaded in memory.
* Each process is allowed to access a subset of the available physical memory.
* Processes can share a single memory image of a library or program.
* Programs can be relocatable — that is, they can be placed anywhere in physical memory.
* Programmers can write machine-independent code, because they do not need to be concerned about physical memory organization.

The main ingredient of a virtual memory subsystem is the notion of *virtual address space*.
The set of memory references that a process can use is different from physical memory addresses.
When a process uses a virtual address, the kernel and the MMU cooperate to find the actual physical location of the requested memory item.

##### Random Access Memory Usage

All Unix operating systems clearly distinguish between two portions of the random access memory (RAM).
A few megabytes are dedicated to storing the kernel image (i.e., the kernel code and the kernel static data structures).
The remaining portion of RAM is usually handled by the virtual memory system and is used in three possible ways:

##### Kernel Memory Allocator

##### Process Virtual Address Space Handling

##### Caching

A good part of the available physical memory is used as cache for hard disks and other block devices.
This is because hard drives are very slow: a disk access requires several milliseconds, which is a very long time compared with the RAM access time.
Therefore, disks are often the bottleneck in system performance.
As a general rule, one of the policies already implemented in the earliest Unix system is to defer writing to disk as long as possible.
As a result, data read previously from disk and no longer used by any process continue to stay in RAM.

#### Device Drivers

## Chapter 2 Memory Addressing

### Memory Addresses

The Memory Management Unit (MMU) transforms a logical address into a linear address by means of a hardware circuit called a segmentation unit;
subsequently, a second hardware circuit called a paging unit transforms the linear address into a physical address

### Segmentation in Hardware

#### Segment Selectors and Segmentation Registers

A logical address consists of two parts: a segment identifier and an offset that specifies the relative address within the segment.
The segment identifier is a 16-bit field called the *Segment Selector*, while the offset is a 32-bit field.

To make it easy to retrieve segment selectors quickly, the processor provides segmentation registers whose only purpose is to hold Segment Selectors;
these registers are called **cs**, **ss**, **ds**, **es**, **fs**, and **gs**.
Although there are only six of them, a program can reuse the same segmentation register for different purposes by saving its content in memory and then restoring it later.

The remaining three segmentation registers are general purpose  and may refer to arbitrary data segments.

The cs register has another important function: it includes a 2-bit field that specifies the Current Privilege Level (CPL) of the CPU.
The value 0 denotes the highest privilege level, while the value 3 denotes the lowest one.
Linux uses only levels 0 and 3, which are respectively called Kernel Mode and User Mode.

#### Segment Descriptors

Each segment is represented by an 8-byte *Segment Descriptor* that describes the segment characteristics.
Segment Descriptors are stored either in the Global Descriptor Table (GDT) or in the Local Descriptor Table (LDT).

### Segmentation in Linux

### Paging in Hardware

The paging unit translates linear addresses into physical ones.
One key task in the unit is to check the requested access type against the access rights of the linear address.
If the memory access is not valid, it generates a Page Fault exception

## Chapter 10 System Calls

## Chapter 11 Signals

Signals were introduced by the first Unix systems to allow interactions between User Mode processes;
the kernel also uses them to notify processes of system events.

### The Role of Signals

A *signal* is a very short message that may be sent to a process or a group of processes.
The only information given to the process is usually a number identifying the signal;
there is no room in standard signals for arguments, a message, or other accompanying information.

A set of macros whose names start with the prefix `SIG` is used to identify signals;
we have already made a few references to them in previous chapters.

Signals serve two main purposes:
* To make a process aware that a specific event has occurred
* To cause a process to execute a *signal handler* function included in its code

Of course, the two purposes are not mutually exclusive, because often a process must react to some event by executing a specific routine.

| # | Signal Name | Default action | Comment | POSIX |
| --- | --- | --- | --- | --- |
| 1 | SIGHUP | Terminate | Hang up controlling terminal or process | Yes |
| 2 | SIGINT | Terminate | Interrupt from keyboard | Yes |

#### Actions Performed upon Delivering a Signal

There are three ways in which a process can respond to a signal:
1. Explicitly ignore the signal.
1. Execute the default action associated with the signal.
This action, which is predefined by the kernel, depends on the signal type and may be any one of the following:
Terminate
Dump
Ignore
Stop
Continue
1. Catch the signal by invoking a corresponding signal-handler function.

Notice that blocking a signal is different from ignoring it.
A signal is not delivered as long as it is blocked;
it is delivered only after it has been unblocked.
An ignored signal is always delivered, and there is no further action.

The `SIGKILL` and `SIGSTOP` signals cannot be ignored, caught, or blocked, and their default actions must always be executed.
Therefore, `SIGKILL` and `SIGSTOP` allow a user with appropriate privileges to terminate and to stop, respectively, every process, regardless of the defenses taken by the program it is executing.

#### POSIX Signals and Multithreaded Applications

#### Data Structures Associated with Signals

For each process in the system, the kernel must keep track of what signals are currently pending or masked;
the kernel must also keep track of how every thread group is supposed to handle every signal.
To do this, the kernel uses several data structures accessible from the process descriptor.

### Generating a Signal

### Delivering a Signal

### System Calls Related to Signal Handling

#### The `kill()` System Call

## Chapter 12 The Virtual Filesystem

### The Role of the VFS

### VFS Data Structures

## Chapter 19 Process Communication

### Pipes

Pipes are an interprocess communication mechanism that is provided in all flavors of Unix.
A pipe is a one-way flow of data between processes: all data written by a process to the pipe is routed by the kernel to another process, which can thus read it.

#### Using a Pipe

Many Unix systems provide, besides the `pipe()` system call, two wrapper functions named `popen()` and `pclose()` that handle all the dirty work        usually done when using pipes.
Once a pipe has been created by means of the `popen()` function, it can be used with the high-level I/O functions included in the C library (`fprintf()`, `fscanf()`, and so on).

In Linux, `popen()` and `pclose()` are included in the C library.
The `popen( )` function receives two parameters: the filename pathname of an executable file and a type string specifying the direction of the data transfer.
It returns the pointer to a FILE data structure.
