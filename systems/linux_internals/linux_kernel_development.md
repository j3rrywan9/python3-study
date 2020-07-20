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
In modern systems, however, multithreaded programs—those that consist of more than one thread — are common.
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
