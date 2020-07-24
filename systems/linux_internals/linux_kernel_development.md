# Linux Kernel Development, Third Edition

## Process Management

Because running user applications is the reason we have operating systems, the process management is a crucial part of any operating system kernel, including Linux.

### The Process

A *process* is a program (object code stored on some media) in the midst of execution.
Processes are, however, more than just the executing program code (often called the text section in Unix).
They also include a set of resources such as open files and pending signals, internal kernel data, processor state, a memory address space with one or more memory mappings, one or more threads of execution, and a data section containing global variables.
Processes, in effect, are the living result of running program code.
The kernel needs to manage all these details efficiently and transparently.

Threads of execution, often shortened to threads, are the objects of activity within the process.
Each thread includes a unique program counter, process stack, and set of processor registers.
The kernel schedules individual threads, not processes.
In traditional Unix systems, each process consists of one thread.
In modern systems, however, multithreaded programs—those that consist of more than one thread - are common.
As you will see later, Linux has a unique implementation of threads: It does not differentiate between threads and processes.
To Linux, a thread is just a special kind of process.

On modern operating systems, processes provide two virtualizations: a virtualized processor and virtual memory.
The virtual processor gives the process the illusion that it alone monopolizes the system, despite possibly sharing the processor among hundreds of other processes.
Virtual memory lets the process allocate and manage memory as if it alone owned all the memory in the system.
Interestingly, note that threads share the virtual memory abstraction, whereas each receives its own virtualized processor.

A process begins its life when, not surprisingly, it is created.
In Linux, this occurs by means of the `fork()` system call, which creates a new process by duplicating an existing one.
The process that calls `fork()` is the *parent*, whereas the new process is the *child*.
The parent resumes execution and the child starts execution at the same place: where the call to `fork()` returns.
The `fork()` system call returns from the kernel twice: once in the parent process and again in the newborn child.

Often, immediately after a fork it is desirable to execute a new, different program.
The `exec()` family of function calls creates a new address space and loads a new program into it.
In contemporary Linux kernels, `fork()` is actually implemented via the `clone()` system call, which is discussed in a following section.

Finally, a program exits via the `exit()` system call.
This function terminates the process and frees all its resources.
A parent process can inquire about the status of a terminated child via the `wait4()` system call, which enables a process to wait for the termination of a specific process.
When a process exits, it is placed into a special zombie state that represents terminated processes until the parent calls `wait()` or `waitpid()`.

### Process Descriptor and The Task Structure

The kernel stores the list of processes in a circular doubly linked list called the *task list*.
Each element in the task list is a *process descriptor* of the type `struct task_struct`, which is defined in `<linux/sched.h>`.
The process descriptor contains all the information about a specific process.

#### Allocating the Process Descriptor

The `task_struct` structure is allocated via the *slab allocator* to provide object reuse and cache coloring.

#### Storing the Process Descriptor

The system identifies processes by a unique *process identification* value or *PID*.
The PID is a numerical value represented by the opaque type `pid_t`, which is typically an `int`.
Because of backward compatibility with earlier Unix and Linux versions, however, the default maximum value is only 32,768 (that of a short int), although the value optionally can be increased as high as four million (this is controlled in `<linux/threads.h>`).
The kernel stores this value as pid inside each process descriptor.

Inside the kernel, tasks are typically referenced directly by a pointer to their `task_struct` structure.
In fact, most kernel code that deals with processes works directly with `struct task_struct`.
Consequently, it is useful to be able to quickly look up the process descriptor of the currently executing task, which is done via the `current` macro.
This macro must be independently implemented by each architecture.
Some architectures save a pointer to the task_struct structure of the currently running process in a register, enabling for efficient access.
Other architectures, such as x86 (which has few registers to waste), make use of the fact that `struct thread_info` is stored on the kernel stack to calculate the location of `thread_info` and subsequently the `task_struct`.

#### Process State

The state field of the process descriptor describes the current condition of the process.
Each process on the system is in exactly one of five different states.
This value is represented by one of five flags:
* `TASK_RUNNING` - The process is runnable;
it is either currently running or on a runqueue waiting to run.
This is the only possible state for a process executing in user-space;
it can also apply to a process in kernel-space that is actively running.
* `TASK_INTERRUPTABLE`
* `TASK_INTERRUPTIBLE`
* `__TASK_STOPPED`
* `__TASK_TRACED`

#### Process Context

One of the most important parts of a process is the executing program code.
This code is read in from an *executable file* and executed within the program's address space.
Normal program execution occurs in *user-space*.
When a program executes a system call or triggers an exception, it enters *kernel-space*.
At this point, the kernel is said to be "executing on behalf of the process" and is in *process context*.
When in process context, the `current` macro is valid.
Upon exiting the kernel, the process resumes execution in user-space, unless a higher-priority process has become runnable in the interim, in which case the scheduler is invoked to select the higher priority process.

System calls and exception handlers are well-defined interfaces into the kernel.
A process can begin executing in kernel-space only through one of these interfaces — *all* access to the kernel is through these interfaces.

#### The Process Family Tree

A distinct hierarchy exists between processes in Unix systems, and Linux is no exception.
All processes are descendants of the `init` process, whose PID is 1.
The kernel starts init in the last step of the boot process.
The init process, in turn, reads the system *initscripts* and executes more programs, eventually completing the boot process.

Every process on the system has exactly one parent.
Likewise, every process has zero or more children.
Processes that are all direct children of the same parent are called *siblings*.
The relationship between processes is stored in the process descriptor.
Each `task_struct` has a pointer to the parent's `task_struct`, named `parent`, and a list of children, named `children`.

The `init` task's process descriptor is statically allocated as `init_task`.
A good example of the relationship between all processes is the fact that this code will always succeed:
```c
struct task_struct *task;

for (task = current; task != &init_task; task = task->parent)
    ;
/* task now points to init */
```

In fact, you can follow the process hierarchy from any one process in the system to any other.
Oftentimes, however, it is desirable simply to iterate over all processes in the system.
This is easy because the task list is a circular, doubly linked list.
To obtain the next task in the list, given any valid task, use
```c
list_entry(task->tasks.next, struct task_struct, tasks)
```

Obtaining the previous task works the same way:
```c
list_entry(task->tasks.prev, struct task_struct, tasks)
```

These two routines are provided by the macros `next_task(task)` and `prev_task(task)`, respectively.
Finally, the macro `for_each_process(task)` is provided, which iterates over the entire task list.

### Process Creation

Process creation in Unix is unique.
Most operating systems implement a spawn mechanism to create a new process in a new address space, read in an executable, and begin executing it.
Unix takes the unusual approach of separating these steps into two distinct functions: `fork()` and `exec()`.
The first, `fork()`, creates a child process that is a copy of the current task.
It differs from the parent only in its PID (which is unique), its PPID (parent's PID, which is set to the original process), and certain resources and statistics, such as pending signals, which are not inherited.
The second function, `exec()`, loads a new executable into the address space and begins executing it.
The combination of `fork()` followed by `exec()` is similar to the single function most operating systems provide.

#### Copy-on-write

Traditionally, upon `fork()`, all resources owned by the parent are duplicated and the copy is given to the child.
This approach is naive and inefficient in that it copies much data that might otherwise be shared.
Worse still, if the new process were to immediately execute a new image, all that copying would go to waste.
In Linux, `fork()` is implemented through the use of copy-on-write pages.
Copy-on-write (or COW) is a technique to delay or altogether prevent copying of the data.
Rather than duplicate the process address space, the parent and the child can share a single copy.

The data, however, is marked in such a way that if it is written to, a duplicate is made and each process receives a unique copy.
Consequently, the duplication of resources occurs only when they are written;
until then, they are shared read-only.
This technique delays the copying of each page in the address space until it is actually written to.
In the case that the pages are never written — for example, if `exec()` is called immediately after `fork()` — they never need to be copied.
The only overhead incurred by `fork()` is the duplication of the parent's page tables and the creation of a unique process descriptor for the child.
In the common case that a process executes a new executable image immediately after forking, this optimization prevents the wasted copying of large amounts of data (with the address space, easily tens of megabytes).
This is an important optimization because the Unix philosophy encourages quick process execution.

#### Forking

Linux implements `fork()` via the `clone()` system call.
This call takes a series of flags that specify which resources, if any, the parent and child process should share.

The bulk of the work in forking is handled by `do_fork()`, which is defined in `kernel/fork.c`.
This function calls `copy_process()` and then starts the process running.
The interesting work is done by copy_process():
1. It calls `dup_task_struct()`, which creates a new kernel stack, `thread_info` structure, and `task_struct` for the new process.
The new values are identical to those of the current task.
At this point, the child and parent process descriptors are identical.
1. It then checks that the new child will not exceed the resource limits on the number of processes for the current user.
1. The child needs to differentiate itself from its parent.
Various members of the process descriptor are cleared or set to initial values.
Members of the process descriptor not inherited are primarily statistically information.
The bulk of the values in `task_struct` remain unchanged.
1. The child's state is set to `TASK_UNINTERRUPTIBLE` to ensure that it does not yet run.
1. `copy_process()` calls `copy_flags()` to update the flags member of the `task_struct`.
The `PF_SUPERPRIV` flag, which denotes whether a task used superuser privileges, is cleared.
The `PF_FORKNOEXEC` flag, which denotes a process that has not called `exec()`, is set.
1. It calls `alloc_pid()` to assign an available PID to the new task.
1. Depending on the flags passed to `clone()`, `copy_process()` either duplicates or shares open files, filesystem information, signal handlers, process address space, and namespace.
These resources are typically shared between threads in a given process;
otherwise they are unique and thus copied here.
1. Finally, `copy_process()` cleans up and returns to the caller a pointer to the new child.

Back in `do_fork()`, if `copy_process()` returns successfully, the new child is woken up and run.
Deliberately, the kernel runs the child process first.
In the common case of the child simply calling `exec()` immediately, this eliminates any copy-on-write overhead that would occur if the parent ran first and began writing to the address space.

The `vfork()` system call has the same effect as `fork()`, except that the page table entries of the parent process are not copied.
Instead, the child executes as the sole thread in the parent's address space, and the parent is blocked until the child either calls `exec()` or exits.

### The Linux Implementation of Threads

Threads are a popular modern programming abstraction.
They provide multiple threads of execution within the same program in a shared memory address space.
They can also share open files and other resources.
Threads enable concurrent programming and, on multiple processor systems, true parallelism.

Linux has a unique implementation of threads.
To the Linux kernel, there is no concept of a thread.
Linux implements all threads as standard processes.
The Linux kernel does not provide any special scheduling semantics or data structures to represent threads.
Instead, a thread is merely a process that shares certain resources with other processes.
Each thread has a unique `task_struct` and appears to the kernel as a normal process — threads just happen to share resources, such as an address space, with other processes.

To Linux, threads are simply a manner of sharing resources between processes (which are already quite lightweight).

#### Creating Threads

Threads are created the same as normal tasks, with the exception that the `clone()` system call is passed flags corresponding to the specific resources to be shared:
```c
clone(CLONE_VM | CLONE_FS | CLONE_FILES | CLONE_SIGHAND, 0);
```

The previous code results in behavior identical to a normal `fork()`, except that the address space, filesystem resources, file descriptors, and signal handlers are shared.
In other words, the new task and its parent are what are popularly called *threads*.

#### Kernel Threads

It is often useful for the kernel to perform some operations in the background.
The kernel accomplishes this via kernel threads — standard processes that exist solely in kernel-space.
The significant difference between kernel threads and normal processes is that kernel threads do not have an address space.
(Their `mm` pointer, which points at their address space, is `NULL`.)
They operate only in kernel-space and do not context switch into user-space.
Kernel threads, however, are schedulable and preemptable, the same as normal processes.

Linux delegates several tasks to kernel threads, most notably the *flush* tasks and the *ksoftirqd* task.
You can see the kernel threads on your Linux system by running the command `ps -ef`.
There are a lot of them!
Kernel threads are created on system boot by other kernel threads.
Indeed, a kernel thread can be created only by another kernel thread.
The kernel handles this automatically by forking all new kernel threads off of the *kthreadd* kernel process.

### Process Termination

When a process terminates, the kernel releases the resources owned by the process and notifies the child's parent of its demise.

Generally, process destruction is self-induced.
It occurs when the process calls the `exit()` system call, either explicitly when it is ready to terminate or implicitly on return from the main subroutine of any program.
(That is, the C compiler places a call to `exit()` after `main()` returns.)
A process can also terminate involuntarily.
This occurs when the process receives a signal or exception it cannot handle or ignore.
Regardless of how a process terminates, the bulk of the work is handled by `do_exit()`, defined in `kernel/exit.c`, which completes a number of chores:
1. It sets the `PF_EXITING` flag in the flags member of the `task_struct`.
1. It calls `del_timer_sync()` to remove any kernel timers.
Upon return, it is guaranteed that no timer is queued and that no timer handler is running.
1. If BSD process accounting is enabled, `do_exit()` calls `acct_update_integrals()` to write out accounting information.
1. It calls `exit_mm()` to release the `mm_struct` held by this process.
If no other process is using this address space — that it, if the address space is not shared — the kernel then destroys it.
1. It calls `exit_sem()`.
If the process is queued waiting for an IPC semaphore, it is dequeued here.
1. It then calls `exit_files()` and `exit_fs()` to decrement the usage count of objects related to file descriptors and filesystem data, respectively.
If either usage counts reach zero, the object is no longer in use by any process, and it is destroyed.
1. It sets the task's exit code, stored in the `exit_code` member of the `task_struct`, to the code provided by `exit()` or whatever kernel mechanism forced the termination.
The exit code is stored here for optional retrieval by the parent.
1. It calls `exit_notify()` to send signals to the task's parent, reparents any of the task's children to another thread in their thread group or the init process, and sets the task's exit state, stored in `exit_state` in the `task_struct` structure, to `EXIT_ZOMBIE`.
1. `do_exit()` calls `schedule()` to switch to a new process.
Because the process is now not schedulable, this is the last code the task will ever execute.
`do_exit()` never returns.

At this point, all objects associated with the task (assuming the task was the sole user) are freed.
The task is not runnable (and no longer has an address space in which to run) and is in the `EXIT_ZOMBIE` exit state.
The only memory it occupies is its kernel stack, the `thread_info` structure, and the `task_struct` structure.
The task exists solely to provide information to its parent.
After the parent retrieves the information, or notifies the kernel that it is uninterested, the remaining memory held by the process is freed and returned to the system for use.

#### Removing the Process Descriptor

After `do_exit()` completes, the process descriptor for the terminated process still exists, but the process is a zombie and is unable to run.
As discussed, this enables the system to obtain information about a child process after it has terminated.
Consequently, the acts of cleaning up after a process and removing its process descriptor are separate.
After the parent has obtained information on its terminated child, or signified to the kernel that it does not care, the child's `task_struct` is deallocated.

#### The Dilemma of the Parentless Task

If a parent exits before its children, some mechanism must exist to reparent any child tasks to a new process, or else parentless terminated processes would forever remain zombies, wasting system memory.
The solution is to reparent a task's children on exit to either another process in the current thread group or, if that fails, the init process.
`do_exit()` calls `exit_notify()`, which calls `forget_original_parent()`, which, in turn, calls `find_new_reaper()` to perform the reparenting:

With the process successfully reparented, there is no risk of stray zombie processes.
The `init` process routinely calls `wait()` on its children, cleaning up any zombies assigned to it.

## Process Scheduling

## System Calls

In any modern operating system, the kernel provides a set of interfaces by which processes running in user-space can interact with the system.
These interfaces give applications controlled access to hardware, a mechanism with which to create new processes and communicate with existing ones, and the capability to request other operating system resources.
The interfaces act as the messengers between applications and the kernel, with the applications issuing various requests and the kernel fulfilling them (or returning an error).
The existence of these interfaces, and the fact that applications are not free to directly do whatever they want, is key to providing a stable system.

### Communicating with the Kernel

System calls provide a layer between the hardware and user-space processes.
This layer serves three primary purposes.
First, it provides an abstracted hardware interface for user-space.
When reading or writing from a file, for example, applications are not concerned with the type of disk, media, or even the type of filesystem on which the file resides.
Second, system calls ensure system security and stability.
With the kernel acting as a middleman between system resources and user-space, the kernel can arbitrate access based on permissions, users, and other criteria.
For example, this arbitration prevents applications from incorrectly using hardware, stealing other processes' resources, or otherwise doing harm to the system.
Finally, a single common layer between user-space and the rest of the system allows for the virtualized system provided to processes.
If applications were free to access system resources without the kernel's knowledge, it would be nearly impossible to implement multitasking and virtual memory, and certainly impossible to do so with stability and security.
In Linux, system calls are the only means user-space has of interfacing with the kernel;
they are the only legal entry point into the kernel other than exceptions and traps.
Indeed, other interfaces, such as device files or `/proc`, are ultimately accessed via system calls.
Interestingly, Linux implements far fewer system calls than most systems.
This chapter addresses the role and implementation of system calls in Linux.

### APIs, POSIX, and the C Library

Typically, applications are programmed against an Application Programming Interface (API) implemented in user-space, not directly to system calls.
This is important because no direct correlation is needed between the interfaces that applications make use of and the actual interface provided by the kernel.
An API defines a set of programming interfaces used by applications.
Those interfaces can be implemented as a system call, implemented through multiple system calls, or implemented without the use of system calls at all.
The same API can exist on multiple systems and provide the same interface to applications while the implementation of the API itself can differ greatly from system to system.

One of the more common application programming interfaces in the Unix world is based on the POSIX standard.
Technically, POSIX is composed of a series of standards from the IEEE that aim to provide a portable operating system standard roughly based on Unix.
Linux strives to be POSIX- and SUSv3-compliant where applicable.

POSIX is an excellent example of the relationship between APIs and system calls.
On most Unix systems, the POSIX-defined API calls have a strong correlation to the system calls.
Indeed, the POSIX standard was created to resemble the interfaces provided by earlier Unix systems.
On the other hand, some systems that are rather un-Unix, such as Microsoft Windows, offer POSIX-compatible libraries.

The system call interface in Linux, as with most Unix systems, is provided in part by the C library.
The C library implements the main API on Unix systems, including the standard C library and the system call interface.
The C library is used by all C programs and, because of C's nature, is easily wrapped by other programming languages for use in their programs.
The C library additionally provides the majority of the POSIX API.

From the application programmer’s point of view, system calls are irrelevant;
all the programmer is concerned with is the API.
Conversely, the kernel is concerned only with the system calls;
what library calls and applications make use of the system calls is not of the kernel's concern.
Nonetheless, it is important for the kernel to keep track of the potential uses of a system call and keep the system call as general and flexible as possible.
A meme related to interfaces in Unix is "Provide mechanism, not policy."
In other words, Unix system calls exist to provide a specific function in an abstract sense.
The manner in which the function is used is not any of the kernel's business.

### syscalls

System calls (often called *syscalls* in Linux) are typically accessed via function calls defined in the C library.
They can define zero, one, or more arguments (inputs) and might result in one or more side effects, for example writing to a file or copying some data into a provided pointer.
System calls also provide a return value of type `long` that signifies success or error — usually, although not always, a negative return value denotes an error.
A return value of zero is usually (but again not always) a sign of success.
The C library, when a system call returns an error, writes a special error code into the global `errno` variable.
This variable can be translated into human-readable errors via library functions such as `perror()`.

Finally, system calls have a defined behavior.
For example, the system call `getpid()` is defined to return an integer that is the current process's PID.

Note that the definition says nothing of the implementation.
The kernel must provide the intended behavior of the system call but is free to do so with whatever implementation it wants as long as the result is correct.
Of course, this system call is as simple as they come, and there are not too many other ways to implement it.

#### System Call Numbers

In Linux, each system call is assigned a syscall number.
This is a unique number that is used to reference a specific system call.
When a user-space process executes a system call, the syscall number identifies which syscall was executed;
the process does not refer to the syscall by name.
The syscall number is important;
when assigned, it cannot change, or compiled applications will break.
Likewise, if a system call is removed, its system call number cannot be recycled, or previously compiled code would aim to invoke one system call but would in reality invoke another.
Linux provides a "not implemented" system call, `sys_ni_syscall()`, which does nothing except return `-ENOSYS`, the error corresponding to an invalid system call.
This function is used to "plug the hole" in the rare event that a syscall is removed or otherwise made unavailable.

The kernel keeps a list of all registered system calls in the system call table, stored in `sys_call_table`.
This table is architecture;
on x86-64 it is defined in `arch/i386/kernel/syscall_64.c`.
This table assigns each valid syscall to a unique syscall number.

#### System Call Performance

System calls in Linux are faster than in many other operating systems.
This is partly because of Linux's fast context switch times
 entering and exiting the kernel is a streamlined and simple affair.
The other factor is the simplicity of the system call handler and the individual system calls themselves.

### System Call Handler

It is not possible for user-space applications to execute kernel code directly.
They cannot simply make a function call to a method existing in kernel-space because the kernel exists in a protected memory space.
If applications could directly read and write to the kernel's address space, system security and stability would be nonexistent.

Instead, user-space applications must somehow signal to the kernel that they want to execute a system call and have the system switch to kernel mode, where the system call can be executed in kernel-space by the kernel on behalf of the application.

The mechanism to signal the kernel is a software interrupt: Incur an exception, and the system will switch to kernel mode and execute the exception handler.
The exception handler, in this case, is actually the system call handler.
The defined software interrupt on x86 is interrupt number 128, which is incurred via the `int $0x80` instruction.
It triggers a switch to kernel mode and the execution of exception vector 128, which is the system call handler.
The system call handler is the aptly named function `system_call()`.
It is architecture-dependent;
on x86-64 it is implemented in assembly in `entry_64.S`.
Recently, x86 processors added a feature known as *sysenter*.
This feature provides a faster, more specialized way of trapping into a kernel to execute a system call than using the int interrupt instruction.
Support for this feature was quickly added to the kernel.
Regardless of how the system call handler is invoked, however, the important notion is that somehow user-space causes an exception or trap to enter the kernel.

#### Denoting the Correct System Call

Simply entering kernel-space alone is not sufficient because multiple system calls exist, all of which enter the kernel in the same manner.
Thus, the system call number must be passed into the kernel.
On x86, the syscall number is fed to the kernel via the `eax` register.
Before causing the trap into the kernel, user-space sticks in `eax` the number corresponding to the desired system call.
The system call handler then reads the value from `eax`.
Other architectures do something similar.

#### Parameter Passing

In addition to the system call number, most syscalls require that one or more parameters be passed to them.
Somehow, user-space must relay the parameters to the kernel during the trap.
The easiest way to do this is via the same means that the syscall number is passed: The parameters are stored in registers.
On x86-32, the registers `ebx`, `ecx`, `edx`, `esi`, and `edi` contain, in order, the first five arguments.
In the unlikely case of six or more arguments, a single register is used to hold a pointer to user-space where all the parameters are stored.

The return value is sent to user-space also via register.
On x86, it is written into the `eax` register.

### System Call Implementation

The actual implementation of a system call in Linux does not need to be concerned with the behavior of the system call handler.
Thus, adding a new system call to Linux is relatively easy.
The hard work lies in designing and implementing the system call;
registering it with the kernel is simple.
Let's look at the steps involved in writing a new system call for Linux.

#### Implementing System Calls

#### Verifying the Parameters

System calls must carefully verify all their parameters to ensure that they are valid and legal.
The system call runs in kernel-space, and if the user can pass invalid input into the kernel without restraint, the system's security and stability can suffer.

### System Call Context

#### Final Steps in Binding a System Call

After the system call is written, it is trivial to register it as an official system call:
1. Add an entry to the end of the system call table.
This needs to be done for each architecture that supports the system call (which, for most calls, is all the architectures).
The position of the syscall in the table, starting at zero, is its system call number.
For example, the tenth entry in the list is assigned syscall number nine.
1. For each supported architecture, define the syscall number in `<asm/unistd.h>`.
1. Compile the syscall into the kernel image (as opposed to compiling as a module).
This can be as simple as putting the system call in a relevant file in `kernel/`, such as `sys.c`, which is home to miscellaneous system calls.

Although it is not explicitly specified, the system call is then given the next subsequent syscall number—in this case, 338.
For each architecture you want to support, the system call must be added to the architecture's system call table.
The system call does not need to receive the same syscall number under each architecture, as the system call number is part of the architecture's unique ABI.
Usually, you would want to make the system call available to each architecture.
Note the convention of placing the number in a comment every five entries;
this makes it easy to find out which syscall is assigned which number.

#### Accessing the System Call from User-Space

## Kernel Data Structures

## Interrupts and Interrupt Handlers

A core responsibility of any operating system kernel is managing the hardware connected to the machine—hard drives and Blu-ray discs, keyboards and mice, 3D processors and wireless radios.
To meet this responsibility, the kernel needs to communicate with the machine's individual devices.
Given that processors can be orders of magnitudes faster than the hardware they talk to, it is not ideal for the kernel to issue a request and wait for a response from the significantly slower hardware.
Instead, because the hardware is comparatively slow to respond, the kernel must be free to go and handle other work, dealing with the hardware only after that hardware has actually completed its work.

How can the processor work with hardware without impacting the machine's overall performance?
One answer to this question is *polling*.
Periodically, the kernel can check the status of the hardware in the system and respond accordingly.
Polling incurs overhead, however, because it must occur repeatedly regardless of whether the hardware is active or ready.
A better solution is to provide a mechanism for the hardware to signal to the kernel when attention is needed.
This mechanism is called an *interrupt*.
In this chapter, we discuss interrupts and how the kernel responds to them, with special functions called *interrupt handlers*.

### Interrupts

Interrupts enable hardware to signal to the processor.
For example, as you type, the keyboard controller (the hardware device that manages the keyboard) issues an electrical signal to the processor to alert the operating system to newly available key presses.
These electrical signals are interrupts.
The processor receives the interrupt and signals the operating system to enable the operating system to respond to the new data.
Hardware devices generate interrupts asynchronously with respect to the processor clock — they can occur at any time.
Consequently, the kernel can be interrupted at any time to process interrupts.

An interrupt is physically produced by electronic signals originating from hardware devices and directed into input pins on an interrupt controller, a simple chip that multiplexes multiple interrupt lines into a single line to the processor.
Upon receiving an interrupt, the interrupt controller sends a signal to the processor.
The processor detects this signal and interrupts its current execution to handle the interrupt.
The processor can then notify the operating system that an interrupt has occurred, and the operating system can handle the interrupt appropriately.

Different devices can be associated with different interrupts by means of a unique value associated with each interrupt.
This way, interrupts from the keyboard are distinct from interrupts from the hard drive.
This enables the operating system to differentiate between interrupts and to know which hardware device caused which interrupt.
In turn, the operating system can service each interrupt with its corresponding handler.
These interrupt values are often called *interrupt request (IRQ)* lines.
Each IRQ line is assigned a numeric value—for example, on the classic PC, IRQ 0 is the timer interrupt and IRQ 1 is the keyboard interrupt.
Not all interrupt numbers, however, are so rigidly defined.
Interrupts associated with devices on the PCI bus, for example, generally are dynamically assigned.
Other non-PC architectures have similar dynamic assignments for interrupt values.
The important notion is that a specific interrupt is associated with a specific device, and the kernel knows this.

### Interrupt Handlers

The function the kernel runs in response to a specific interrupt is called an interrupt handler or *interrupt service routine (ISR)*.
Each device that generates interrupts has an associated interrupt handler.
For example, one function handles interrupts from the system timer, whereas another function handles interrupts generated by the keyboard.
The interrupt handler for a device is part of the device's *driver* - the kernel code that manages the device.

In Linux, interrupt handlers are normal C functions.
They match a specific prototype, which enables the kernel to pass the handler information in a standard way, but otherwise they are ordinary functions.
What differentiates interrupt handlers from other kernel functions is that the kernel invokes them in response to interrupts and that they run in a special context called *interrupt context*.
This special context is occasionally called *atomic context* because, as we shall see, code executing in this context is unable to block.
In this book, we will use the term interrupt context.

Because an interrupt can occur at any time, an interrupt handler can, in turn, be executed at any time.
It is imperative that the handler runs quickly, to resume execution of the interrupted code as soon as possible.
Therefore, while it is important to the hardware that the operating system services the interrupt without delay, it is also important to the rest of the system that the interrupt handler executes in as short a period as possible.

At the very least, an interrupt handler's job is to acknowledge the interrupt's receipt to the hardware: Hey, hardware, I hear ya; now get back to work!
Often, however, interrupt handlers have a large amount of work to perform.
For example, consider the interrupt handler for a network device.
On top of responding to the hardware, the interrupt handler needs to copy networking packets from the hardware into memory, process them, and push the packets down to the appropriate protocol stack or application.
Obviously, this can be a lot of work, especially with today's gigabit and 10-gigabit Ethernet cards.

### Top Halves vs Bottom Halves

These two goals—that an interrupt handler execute quickly and perform a large amount of work — clearly conflict with one another.
Because of these competing goals, the processing of interrupts is split into two parts, or halves.
The interrupt handler is the *top half*.
The top half is run immediately upon receipt of the interrupt and performs only the work that is time-critical, such as acknowledging receipt of the interrupt or resetting the hardware.
Work that can be performed later is deferred until the *bottom half*.
The bottom half runs in the future, at a more convenient time, with all interrupts enabled.

### Registering an Interrupt Handler

Interrupt handlers are the responsibility of the driver managing the hardware.
Each device has one associated driver and, if that device uses interrupts (and most do), then that driver must register one interrupt handler.

Drivers can register an interrupt handler and enable a given interrupt line for handling with the function `request_irq()`, which is declared in `<linux/interrupt.h>`:

The first parameter, `irq`, specifies the interrupt number to allocate.
For some devices, for example legacy PC devices such as the system timer or keyboard, this value is typically hard-coded.
For most other devices, it is probed or otherwise determined programmatically and dynamically.

The second parameter, `handler`, is a function pointer to the actual interrupt handler that services this interrupt.
This function is invoked whenever the operating system receives the interrupt.
```c
typedef irqreturn_t (*irq_handler_t)(int, void *);
```
Note the specific prototype of the handler function: It takes two parameters and has a return value of `irqreturn_t`.

#### Interrupt Handler Flags

The third parameter, `flags`, can be either zero or a bit mask of one or more of the flags defined in `<linux/interrupt.h>`.
Among these flags, the most important are:
* IRQF_DISABLED - When set, this flag instructs the kernel to disable all interrupts when executing this interrupt handler.
When unset, interrupt handlers run with all interrupts except their own enabled.
Most interrupt handlers do not set this flag, as disabling all interrupts is bad form.
Its use is reserved for performance-sensitive interrupts that execute quickly.
This flag is the current manifestation of the SA_INTERRUPT flag, which in the past distinguished between “fast” and “slow” interrupts.
* IRQF_SAMPLE_RANDOM - This flag specifies that interrupts generated by this device should contribute to the kernel entropy pool.
The kernel entropy pool provides truly random numbers derived from various random events.
If this flag is specified, the timing of interrupts from this device are fed to the pool as entropy.
Do not set this if your device issues interrupts at a predictable rate (for example, the system timer) or can be influenced by external attackers (for example, a networking device).
On the other hand, most other hardware generates interrupts at nondeterministic times and is, therefore, a good source of entropy.
* IRQF_TIMER - This flag specifies that this handler processes interrupts for the system timer.
* IRQF_SHARED - This flag specifies that the interrupt line can be shared among multiple interrupt handlers.
Each handler registered on a given line must specify this flag; otherwise, only one handler can exist per line.
More information on shared handlers is provided in a following section.

The fourth parameter, `name`, is an ASCII text representation of the device associated with the interrupt.
For example, this value for the keyboard interrupt on a PC is keyboard.
These text names are used by `/proc/irq` and `/proc/interrupts` for communication with the user, which is discussed shortly.
The fifth parameter, `dev`, is used for shared interrupt lines.
When an interrupt handler is freed (discussed later), `dev` provides a unique cookie to enable the removal of only the desired interrupt handler from the interrupt line.
Without this parameter, it would be impossible for the kernel to know which handler to remove on a given interrupt line.
You can pass `NULL` here if the line is not shared, but you must pass a unique cookie if your interrupt line is shared.
(And unless your device is old and crusty and lives on the ISA bus, there is a good chance it must support sharing.)
This pointer is also passed into the interrupt handler on each invocation.
A common practice is to pass the driver's device structure: This pointer is unique and might be useful to have within the handlers.

On success, `request_irq()` returns zero.
A nonzero value indicates an error, in which case the specified interrupt handler was not registered.
A common error is `-EBUSY`, which denotes that the given interrupt line is already in use (and either the current user or you did not specify `IRQF_SHARED`).

Note that `request_irq()` can sleep and therefore cannot be called from interrupt context or other situations where code cannot block.
It is a common mistake to call `request_irq()` when it is unsafe to sleep.
This is partly because of *why* `request_irq()` can block: It is indeed unclear.
On registration, an entry corresponding to the interrupt is created in `/proc/irq`.
The function `proc_mkdir()` creates new procfs entries.
This function calls `proc_create()` to set up the new procfs entries, which in turn calls `kmalloc()` to allocate memory.

#### An Interrupt Example

#### Freeing an Interrupt Handler

### Writing an Interrupt Handler

#### Shared Handlers

#### A Real-Life Interrupt Handler

### Interrupt Context

When executing an interrupt handler, the kernel is in *interrupt context*.
Recall that process context is the mode of operation the kernel is in while it is executing on behalf of a process - for example, executing a system call or running a kernel thread.
In process context, the `current` macro points to the associated task.
Furthermore, because a process is coupled to the kernel in process context, process context can sleep or otherwise invoke the scheduler.

Interrupt context, on the other hand, is not associated with a process.
The `current` macro is not relevant (although it points to the interrupted process).
Without a backing process, interrupt context cannot sleep - how would it ever reschedule?
Therefore, you cannot call certain functions from interrupt context.
If a function sleeps, you cannot use it from your interrupt handler - this limits the functions that one can call from an interrupt handler.
Interrupt context is time-critical because the interrupt handler interrupts other code.
Code should be quick and simple.
Busy looping is possible, but discouraged.
This is an important point;
always keep in mind that your interrupt handler has interrupted other code (possibly even another interrupt handler on a different line!).
Because of this asynchronous nature, it is imperative that all interrupt handlers be as quick and as simple as possible.
As much as possible, work should be pushed out from the interrupt handler and performed in a bottom half, which runs at a more convenient time.

### Implementing Interrupt Handlers

Perhaps not surprising, the implementation of the interrupt handling system in Linux is architecture-dependent.
The implementation depends on the processor, the type of interrupt controller used, and the design of the architecture and machine.

A device issues an interrupt by sending an electric signal over its bus to the interrupt controller.
If the interrupt line is enabled (they can be masked out), the interrupt controller sends the interrupt to the processor.
In most architectures, this is accomplished by an electrical signal sent over a special pin to the processor.
Unless interrupts are disabled in the processor (which can also happen), the processor immediately stops what it is doing, disables the interrupt system, and jumps to a predefined location in memory and executes the code located there.
This predefined point is set up by the kernel and is the *entry point* for interrupt handlers.

#### /proc/interrupts

Procfs is a virtual filesystem that exists only in kernel memory and is typically mounted at `/proc`.
Reading or writing files in procfs invokes kernel functions that simulate reading or writing from a real file.
A relevant example is the `/proc/interrupts` file, which is populated with statistics related to interrupts on the system.

For the curious, procfs code is located primarily in `fs/proc`.
The function that provides `/proc/interrupts` is, not surprisingly, architecture-dependent and named `show_interrupts()`.

### Interrupt Control

The Linux kernel implements a family of interfaces for manipulating the state of interrupts on a machine.
These interfaces enable you to disable the interrupt system for the current processor or mask out an interrupt line for the entire machine.
These routines are all architecture-dependent and can be found in `<asm/system.h>` and `<asm/irq.h>`.

Reasons to control the interrupt system generally boil down to needing to provide synchronization.
By disabling interrupts, you can guarantee that an interrupt handler will not preempt your current code.
Moreover, disabling interrupts also disables kernel preemption.
Neither disabling interrupt delivery nor disabling kernel preemption provides any protection from concurrent access from another processor, however.
Because Linux supports multiple processors, kernel code more generally needs to obtain some sort of lock to prevent another processor from accessing shared data simultaneously.
These locks are often obtained in conjunction with disabling local interrupts.
The lock provides protection against concurrent access from another processor, whereas disabling interrupts provides protection against concurrent access from a possible interrupt handler.
Nevertheless, understanding the kernel interrupt control interfaces is important.

## Bottom Halves and Deferring Work

Consequently, managing interrupts is divided into two parts, or *halves*.
The first part, interrupt handlers (*top halves*), are executed by the kernel asynchronously in immediate response to a hardware interrupt, as discussed in the previous chapter.
This chapter looks at the second part of the interrupt solution, *bottom halves*.

### Bottom Halves

The job of bottom halves is to perform any interrupt-related work not performed by the interrupt handler.
In an ideal world, this is nearly all the work because you want the interrupt handler to perform as little work (and in turn be as fast) as possible.
By offloading as much work as possible to the bottom half, the interrupt handler can return control of the system to whatever it interrupted as quickly as possible.

Nonetheless, the interrupt handler must perform some of the work.
For example, the interrupt handler almost assuredly needs to acknowledge to the hardware the receipt of the interrupt.
It may need to copy data to or from the hardware.
This work is timing-sensitive, so it makes sense to perform it in the interrupt handler.

Almost anything else is fair game for performing in the bottom half.
For example, if you copy data from the hardware into memory in the top half, it certainly makes sense to process it in the bottom half.
Unfortunately, no hard and fast rules exist about what work to perform where - the decision is left entirely up to the device-driver author.
Although no arrangement is *illegal*, an arrangement can certainly be *suboptimal*.
Remember, interrupt handlers run asynchronously, with at least the current interrupt line disabled.
Minimizing their duration is important.
Although it is not always clear how to divide the work between the top and bottom half, a couple of useful tips help:
* If the work is time sensitive, perform it in the interrupt handler.
* If the work is related to the hardware, perform it in the interrupt handler.
* If the work needs to ensure that another interrupt (particularly the same interrupt) does not interrupt it, perform it in the interrupt handler.
* For everything else, consider performing the work in the bottom half.

When attempting to write your own device driver, looking at other interrupt handlers and their corresponding bottom halves can help.
When deciding how to divide your interrupt processing work between the top and bottom half, ask yourself what *must* be in the top half and what *can* be in the bottom half.
Generally, the quicker the interrupt handler executes, the better.

## An Introduction to Kernel Synchronization

In a shared memory application, developers must ensure that shared resources are protected from concurrent access.
The kernel is no exception.
Shared resources require protection from concurrent access because if multiple threads of execution1 access and manipulate the data at the same time, the threads may overwrite each other's changes or access data while it is in an inconsistent state.
Concurrent access of shared data is a recipe for instability that often proves hard to track down and debug - getting it right at the start is important.

## Kernel Synchronization Methods

## Timers and Time Management

## Memory Management

Memory allocation inside the kernel is not as easy as memory allocation outside the kernel.
Simply put, the kernel lacks luxuries enjoyed by user-space.
Unlike user-space, the kernel is not always afforded the capability to easily allocate memory.
For example, the kernel cannot easily deal with memory allocation errors, and the kernel often cannot sleep.
Because of these limitations, and the need for a lightweight memory allocation scheme, getting hold of memory in the kernel is more complicated than in user-space.
This is not to say that, from a programmer's point of view, kernel memory allocations are difficult - just different.

This chapter discusses the methods used to obtain memory inside the kernel.
Before you can delve into the actual allocation interfaces, however, you need to understand how the kernel handles memory.

### Pages

The kernel treats physical pages as the basic unit of memory management.
Although the processor's smallest addressable unit is a byte or a word, the memory management unit (MMU, the hardware that manages memory and performs virtual to physical address translations) typically deals in pages.
Therefore, the MMU maintains the system's page tables with page-sized granularity (hence their name).
In terms of virtual memory, pages are the smallest unit that matters.

Many architectures even support multiple page sizes.
Most 32-bit architectures have 4KB pages, whereas most 64-bit architectures have 8KB pages.
This implies that on a machine with 4KB pages and 1GB of memory, physical memory is divided into 262,144 distinct pages.

The kernel represents every physical page on the system with a struct `page` structure.
This structure is defined in `<linux/mm_types.h>`.

The important point to understand is that the page structure is associated with physical pages, not virtual pages.
Therefore, what the structure describes is transient at best.
Even if the data contained in the page continues to exist, it might not always be associated with the same page structure because of swapping and so on.
The kernel uses this data structure to describe the associated physical page.
The data structure's goal is to describe physical memory, not the data contained therein.

The kernel uses this structure to keep track of all the pages in the system, because the kernel needs to know whether a page is free (that is, if the page is not allocated).
If a page is not free, the kernel needs to know who owns the page.
Possible owners include user-space processes, dynamically allocated kernel data, static kernel code, the page cache, and so on.

### Zones

Because of hardware limitations, the kernel cannot treat all pages as identical.
Some pages, because of their physical address in memory, cannot be used for certain tasks.
Because of this limitation, the kernel divides pages into different *zones*.
The kernel uses the zones to group pages of similar properties.
In particular, Linux has to deal with two shortcomings of hardware with respect to memory addressing:
* Some hardware devices can perform DMA (direct memory access) to only certain memory addresses.
* Some architectures can physically addressing larger amounts of memory than they can virtually address.
Consequently, some memory is not permanently mapped into the kernel address space.

Because of these constraints, Linux has four primary memory zones:
* ZONE_DMA - This zone contains pages that can undergo DMA.
* ZONE_DMA32 - Like ZOME_DMA, this zone contains pages that can undergo DMA.
Unlike ZONE_DMA, these pages are accessible only by 32-bit devices.
On some architectures, this zone is a larger subset of memory.
* ZONE_NORMAL - This zone contains normal, regularly mapped, pages.
* ZONE_HIGHMEM - This zone contains "high memory," which are pages not permanently mapped into the kernel's address space.

These zones, and two other, less notable ones, are defined in `<linux/mmzone.h>`.

The actual use and layout of the memory zones is architecture-dependent.
For example, some architectures have no problem performing DMA into any memory address.
In those architectures, `ZONE_DMA` is empty and `ZONE_NORMAL` is used for allocations regardless of their use.
As a counterexample, on the x86 architecture, ISA devices cannot perform DMA into the full 32-bit address space because ISA devices can access only the first 16MB of physical memory.
Consequently, `ZONE_DMA` on x86 consists of all memory in the range 0MB–16MB.

`ZONE_HIGHMEM` works in the same regard.
What an architecture can and cannot directly map varies.
On 32-bit x86 systems, `ZONE_HIGHMEM` is all memory above the physical 896MB mark.
On other architectures, `ZONE_HIGHMEM` is empty because all memory is directly mapped.
The memory contained in `ZONE_HIGHMEM` is called *high memory*.
The rest of the system's memory is called *low memory*.

`ZONE_NORMAL` tends to be whatever is left over after the previous two zones claim their requisite shares.
On x86, for example, `ZONE_NORMAL` is all physical memory from 16MB to 896MB.
On other (more fortunate) architectures, `ZONE_NORMAL` is all available memory.

Linux partitions the system's pages into zones to have a pooling in place to satisfy allocations as needed.
For example, having a `ZONE_DMA` pool gives the kernel the capability to satisfy memory allocations needed for DMA.
If such memory is needed, the kernel can simply pull the required number of pages from `ZONE_DMA`.
Note that the zones do not have any physical relevance but are simply logical groupings used by the kernel to keep track of pages.

Although some allocations may require pages from a particular zone, other allocations may pull from multiple zones.
For example, although an allocation for DMA-able memory must originate from `ZONE_DMA`, a normal allocation can come from `ZONE_DMA` or `ZONE_NORMAL` but not both;
allocations cannot cross zone boundaries.
The kernel prefers to satisfy normal allocations from the normal zone, of course, to save the pages in `ZONE_DMA` for allocations that need it.
But if push comes to shove (say, if memory should get low), the kernel can dip its fingers in whatever zone is available and suitable.

Not all architectures define all zones.
For example, a 64-bit architecture such as Intel's x86-64 can fully map and handle 64-bits of memory.
Thus, x86-64 has no `ZONE_HIGHMEM` and all physical memory is contained within `ZONE_DMA` and `ZONE_NORMAL`.

Each zone is represented by `struct zone`, which is defined in `<linux/mmzone.h>`:

### Getting Pages

Now with an understanding of how the kernel manages memory - via pages, zones, and so on - let's look at the interfaces the kernel implements to enable you to allocate and free memory within the kernel.

#### Getting Zeroed Pages

#### Freeing Pages

These low-level page functions are useful when you need page-sized chunks of physically contiguous pages, especially if you need exactly a single page or two.
For more general byte-sized allocations, the kernel provides `kmalloc()`.

#### `kmalloc()`

The `kmalloc()` function’s operation is similar to that of user-space's familiar `malloc()` routine, with the exception of the additional `flags` parameter.
The `kmalloc()` function is a simple interface for obtaining kernel memory in byte-sized chunks.
If you need whole pages, the previously discussed interfaces might be a better choice.
For most kernel allocations, however, `kmalloc()` is the preferred interface.

The function is declared in `<linux/slab.h>`:
```c
void *kmalloc(size_t size, gfp_t flags)
```
The function returns a pointer to a region of memory that is at least size bytes in length.
The region of memory allocated is physically contiguous.
On error, it returns `NULL`. Kernel allocations always succeed, unless an insufficient amount of memory is available.
Thus, you must check for `NULL` after all calls to `kmalloc()` and handle the error appropriately.

#### `gfp_mask` Flags

You've seen various examples of allocator flags in both the low-level page allocation functions and kmalloc().
Now it's time to discuss these flags in depth.
Flags are represented by the `gfp_t` type, which is defined in `<linux/types.h>` as an `unsigned int`.
*gfp* stands for `__get_free_pages()`, one of the memory allocation routines we discussed earlier.

#### `kfree()`

#### `vmalloc()`

The `vmalloc()` function works in a similar fashion to `kmalloc()`, except it allocates memory that is only virtually contiguous and not necessarily physically contiguous.
This is how a user-space allocation function works: The pages returned by `malloc()` are contiguous within the virtual address space of the processor, but there is no guarantee that they are actually contiguous in physical RAM.
The `kmalloc()` function guarantees that the pages are physically contiguous (and virtually contiguous).
The `vmalloc()` function ensures only that the pages are contiguous within the virtual address space.
It does this by allocating potentially noncontiguous chunks of physical memory and "fixing up" the page tables to map the memory into a contiguous chunk of the logical address space.

### Slab Layer

Allocating and freeing data structures is one of the most common operations inside any kernel.
To facilitate frequent allocations and deallocations of data, programmers often introduce *free lists*.
A free list contains a block of available, already allocated, data structures.
When code requires a new instance of a data structure, it can grab one of the structures off the free list rather than allocate the sufficient amount of memory and set it up for the data structure.
Later, when the data structure is no longer needed, it is returned to the free list instead of deallocated.
In this sense, the free list acts as an object cache, caching a frequently used *type* of object.

One of the main problems with free lists in the kernel is that there exists no global control.
When available memory is low, there is no way for the kernel to communicate to every free list that it should shrink the sizes of its cache to free up memory.
The kernel has no understanding of the random free lists at all.
To remedy this, and to consolidate code, the Linux kernel provides the slab layer (also called the slab allocator).
The slab layer acts as a generic data structure - caching layer.

The concept of a slab allocator was first implemented in Sun Microsystem's SunOS 5.4 operating system.
The Linux data structure caching layer shares the same name and basic design.

## The Virtual Filesystem

### Common Filesystem Interface

The VFS is the glue that enables system calls such as `open()`, `read()`, and `write()` to work regardless of the filesystem or underlying physical medium.
These days, that might not sound novel - we have long been taking such a feature for granted - but it is a nontrivial feat for such generic system calls to work across many diverse filesystems and varying media.
More so, the system calls work *between* these different filesystems and media - we can use standard system calls to copy or move files from one filesystem to another.
In older operating systems, such as DOS, this would never have worked;
any access to a non-native filesystem required special tools.
It is only because modern operating systems, such as Linux, abstract access to the filesystems via a virtual interface that such interoperation and generic access is possible.

New filesystems and new varieties of storage media can find their way into Linux, and programs need not be rewritten or even recompiled.
In this chapter, we will discuss the VFS, which provides the abstraction allowing myriad filesystems to behave as one.
In the next chapter, we will discuss the block I/O layer, which allows various storage devices - CD to Blu-ray discs to hard drives to CompactFlash.
Together, the VFS and the block I/O layer provide the abstractions, interfaces, and glue that allow user-space programs to issue generic system calls to access files via a uniform naming policy on any filesystem, which itself exists on any storage medium.

### Filesystem Abstraction Layer

Such a generic interface for any type of filesystem is feasible only because the kernel implements an abstraction layer around its low-level filesystem interface.
This abstraction layer enables Linux to support different filesystems, even if they differ in supported features or behavior.
This is possible because the VFS provides a common file model that can represent any filesystem's general feature set and behavior.
Of course, it is biased toward Unix-style filesystems.
(You see what constitutes a Unix-style filesystem later in this chapter.)
Regardless, wildly differing filesystem types are still supportable in Linux, from DOS's FAT to Windows's NTFS to many Unix-style and Linux-specific filesystems.

### Unix Filesystems

Historically, Unix has provided four basic filesystem-related abstractions: files, directory entries, inodes, and mount points.

A *filesystem* is a hierarchical storage of data adhering to a specific structure.
Filesystems contain files, directories, and associated control information.
Typical operations performed on filesystems are creation, deletion, and mounting.
In Unix, filesystems are mounted at a specific mount point in a global hierarchy known as a *namespace*.
This enables all mounted filesystems to appear as entries in a single tree.
Contrast this single, unified tree with the behavior of DOS and Windows, which break the file namespace up into drive letters, such as `C:`.
This breaks the namespace up among device and partition boundaries, "leaking" hardware details into the filesystem abstraction.
As this delineation may be arbitrary and even confusing to the user, it is inferior to Linux's unified namespace.

A *file* is an ordered string of bytes.
The first byte marks the beginning of the file, and the last byte marks the end of the file.
Each file is assigned a human-readable name for identification by both the system and the user.
Typical file operations are read, write, create, and delete.

Files are organized in directories.
A *directory* is analogous to a folder and usually contains related files.
Directories can also contain other directories, called subdirectories.
In this fashion, directories may be nested to form paths.
Each component of a path is called a *directory entry*.
In Unix, directories are actually normal files that simply list the files contained therein.
Because a directory is a file to the VFS, the same operations performed on files can be performed on directories.

Unix systems separate the concept of a file from any associated information about it, such as access permissions, size, owner, creation time, and so on.
This information is sometimes called *file metadata* (that is, data about the file's data) and is stored in a separate data structure from the file, called the *inode*.
This name is short for *index node*, although these days the term inode is much more ubiquitous.

### VFS Objects and Their Data Structures

The VFS is object-oriented.
A family of data structures represents the common file model.
These data structures are akin to objects.
Because the kernel is programmed strictly in C, without the benefit of a language directly supporting object-oriented paradigms, the data structures are represented as C structures.
The structures contain both data and pointers to filesystem-implemented functions that operate on the data.

The four primary object types of the VFS are
* The *superblock* object, which represents a specific mounted filesystem.
* The *inode* object, which represents a specific file.
* The *dentry* object, which represents a directory entry, which is a single component of a path.
* The *file* object, which represents an open file as associated with a process.

Note that because the VFS treats directories as normal files, there is not a specific directory object.
Recall from earlier in this chapter that a dentry represents a component in a path, which might include a regular file.
In other words, a dentry is not the same as a directory, but a directory is just another kind of file.

An *operations* object is contained within each of these primary objects.
These objects describe the methods that the kernel invokes against the primary objects:
* The `super_operations` object, which contains the methods that the kernel can invoke on a specific filesystem, such as write_inode() and sync_fs()
* The `inode_operations` object, which contains the methods that the kernel can invoke on a specific file, such as create() and link()
* The `dentry_operations` object, which contains the methods that the kernel can invoke on a specific directory entry, such as d_compare() and d_delete()
* The `file_operations` object, which contains the methods that a process can invoke on an open file, such as read() and write()

The operations objects are implemented as a structure of pointers to functions that operate on the parent object.
For many methods, the objects can inherit a generic function if basic functionality is sufficient.
Otherwise, the specific instance of the particular filesystem fills in the pointers with its own filesystem-specific methods.

Again, note that objects refer to structures—not explicit class types, such as those in C++ or Java.
These structures, however, represent specific instances of an object, their associated data, and methods to operate on themselves.
They are very much objects.

The VFS loves structures, and it is comprised of a couple more than the primary objects previously discussed.
Each registered filesystem is represented by a `file_system_type` structure.
This object describes the filesystem and its capabilities.
Furthermore, each mount point is represented by the `vfsmount` structure.
This structure contains information about the mount point, such as its location and mount flags.

Finally, two per-process structures describe the filesystem and files associated with a process.
They are, respectively, the `fs_struct` structure and the `file` structure.

### The superblock Object

The superblock object is implemented by each filesystem and is used to store information describing that specific filesystem.
This object usually corresponds to the *filesystem superblock* or the *filesystem control block*, which is stored in a special sector on disk (hence the object's name).
Filesystems that are not disk-based (a virtual memory–based filesystem, such as *sysfs*, for example) generate the superblock on-the-fly and store it in memory.

### superblock Operations

The most important item in the superblock object is `s_op`, which is a pointer to the superblock operations table.
The superblock operations table is represented by `struct super_operations` and is defined in `<linux/fs.h>`.

### The inode Object

The inode object represents all the information needed by the kernel to manipulate a file or directory.
For Unix-style filesystems, this information is simply read from the on-disk inode.
If a filesystem does not have inodes, however, the filesystem must obtain the information from wherever it is stored on the disk.
Filesystems without inodes generally store file-specific information as part of the file;
unlike Unix-style filesystems, they do not separate file data from its control information.
Some modern filesystems do neither and store file metadata as part of an on-disk database.
Whatever the case, the inode object is constructed in memory in whatever manner is applicable to the filesystem.

### inode Operations

As with the superblock operations, the `inode_operations` member is important.
It describes the filesystem's implemented functions that the VFS can invoke on an inode.

### The dentry Object

#### dentry State

A valid dentry object can be in one of three states: used, unused, or negative.

#### dentry Cache

### dentry Operations

The `dentry_operations` structure specifies the methods that the VFS invokes on directory entries on a given filesystem.

### The file Object

### file Operations

As with all the other VFS objects, the file operations table is quite important.
The operations associated with `struct file` are the familiar system calls that form the basis of the standard Unix system calls.

### Data Structures Associated with Filesystems

In addition to the fundamental VFS objects, the kernel uses other standard data structures to manage data related to filesystems.
The first object is used to describe a specific variant of a filesystem, such as ext3, ext4, or UDF.
The second data structure describes a mounted instance of a filesystem.

### Data Structures Associated with a Process

Each process on the system has its own list of open files, root filesystem, current working directory, mount points, and so on.
Three data structures tie together the VFS layer and the processes on the system: `files_struct`, `fs_struct`, and `namespace`.

The `files_struct` is defined in `<linux/fdtable.h>`.
This table's address is pointed to by the files entry in the processor descriptor.
All per-process information about open files and file descriptors is contained therein.

The second process-related structure is `fs_struct`, which contains filesystem information related to a process and is pointed at by the `fs` field in the process descriptor.
The structure is defined in `<linux/fs_struct.h>`.

The third and final structure is the `namespace` structure, which is defined in `<linux/mnt_namespace.h>` and pointed at by the mnt_namespace field in the process descriptor.
Per-process namespaces were added to the 2.4 Linux kernel.
They enable each process to have a unique view of the mounted filesystems on the system - not just a unique root directory, but an entirely unique filesystem hierarchy.
