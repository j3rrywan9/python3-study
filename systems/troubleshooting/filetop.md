# filetop

File reads and writes by filename and process.
Top for files.

## Synopsis

```
filetop [-h] [-C] [-r MAXROWS] [-s {reads,writes,rbytes,wbytes}] [-p PID] [interval] [count]
```

## Description

This is top for files.

This traces file reads and writes, and prints a per-file summary every interval (by default, 1 second).
By default the summary is sorted on the highest read throughput (Kbytes).
Sorting order can be changed via -s option. By default only IO on regular files is shown.
The -a option will list all file types (sokets, FIFOs, etc).

This uses in-kernel eBPF maps to store per process summaries for efficiency.

This script works by tracing the `__vfs_read()` and `__vfs_write()` functions using kernel dynamic tracing, which instruments explicit read and write calls.
If files are read or written using another means (eg, via `mmap()`), then they will not be visible using this tool.
Also, this tool will need updating to match any code changes to those vfs functions.

This should be useful for file system workload characterization when analyzing the performance of applications.

Note that tracing VFS level reads and writes can be a frequent activity, and this tool can begin to cost measurable overhead at high I/O rates.

Since this uses BPF, only the root user can use this tool.
