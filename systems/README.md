# Systems

## What to Expect?

The purpose of the systems interview is to understand how well the interviewee understands the inner workings of a Linux system.

It's important to remember that the interviewer's job is to find the limits of your knowledge.
The interviewer will probably keep asking more and more detailed questions until you run out of answers.
If this happens, don't be afraid to say you don't know something.
No one is expected to ace the entire interview.
It's much better to admit you are at the limits of your knowledge and then take an educated guess as to what the answer might be rather than to answer a question incorrectly while pretending that you really know what you are talking about.

The Systems interview generally covers at least one the following topics:
* Linux Internals
* Troubleshooting

Some interviewers may spend the entirety of the interview focused on one topic while others may incorporate both.
They are described in detail below.

## Linux Internals

This portion of the Systems interview is designed to evaluate your knowledge of Unix/Linux internals.
It will assess if you truly understand what is happening under the hood of a Unix/Linux system.
It's very rare that you will be asked questions about how specific software packages like Apache, MySQL, and Chef work.
Lower level systems knowledge is more generic and more transferrable.
If you understand how the system itself works, it's much easier to troubleshoot an application running on top of it.

Topics can include, but are not limited to:
* Process Creation, Execution and Destruction
* Differences between Processes and Threads
* Memory Management
* System Calls
* Signals and Signal Handlers
* Unix Filesystem Structure

### How Successful Candidates Prepare

Review Linux system fundamentals and the topics mentioned above.
A book like "Modern Operating Systems" by Andrew Tanenbaum is a great starting point.
* Review userspace/kernel space boundaries and interactions.
* Examples might include: ioctls, sysctls, context switches.

## Troubleshooting

Understanding how a Unix/Linux system works is one set of skills.
Being able to effectively use that knowledge to troubleshoot a running system is a slightly different set of skills.

For a troubleshooting question, we evaluate your ability to do two things:
* Demonstrate your knowledge of the tools that are available to troubleshoot a system and that you understand the data these tools give you.
* Demonstrate a good approach to troubleshooting a problem.
This means that you can follow a path of investigation where you are progressively ruling out potential problems until you arrive at the root cause of the problem.

In most of these questions, the interviewer will lay out a system related issue or problem that you are seeing in the infrastructure and ask you to troubleshoot it.
Typically, the description of the problem will be vague;
for example, a customer complains that "the system is slow".
The interviewer will ask you how you would like to investigate this problem.
You'll propose a course of action like running a specific command looking for something in the output.
As you take each step, the interviewer will provide the hypothetical system output to prompt you to the next step.

A second scenario might involve having you analyze Linux/Unix system performance using various tools.

No single tool or topic is critical, but a broad familiarity with each of these spaces and the ability to apply that knowledge to new situations is important.
Everything from the kernel to the user space is fair game, and we look for both breadth and depth of knowledge.

The interviewer may share a copy of a report or command output via coderpad.io and the expectation would be for you to understand the data and what it means for a system.

### How Successful Candidates Prepare

* Review troubleshooting tools for system-level performance issues.
* Review troubleshooting tools for debugging application-level performance issues or bugs.

## References

* [SRE Interview Questions](https://syedali.net/engineer-interview-questions/)
* [Linux System Administrator/DevOps Interview Questions](https://github.com/chassing/linux-sysadmin-interview-questions)
* [Linux Insides](https://github.com/0xAX/linux-insides)
