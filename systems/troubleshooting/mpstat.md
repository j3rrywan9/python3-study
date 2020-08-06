# mpstat

Report processors related statistics.

## Synopsis

```
mpstat [ -A ] [ --dec={ 0 | 1 | 2 } ] [ -n ] [ -u ] [ -V ] [ -I { keyword [,...] | ALL } ] [ -N { node_list | ALL } ] [ -o JSON ] [ -P { cpu_list | ALL } ] [ interval [ count ] ]
```

## Description

The **mpstat** command writes to standard output activities for each available processor, processor 0 being the first one.

## Options

```
-P { cpu_list | ALL }
```
Indicate the processors for which statistics are to be reported.
cpu_list is a list of comma-separated values or range of values (e.g., 0,2,4-7,12-).
Note that processor 0 is the  first processor, and processor **all** is the global average among all processors.
The **ALL** keyword indicates that statistics are to be reported for all processors.
Offline processors are not displayed.
