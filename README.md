## This is a repository for the home assigment sent by the company https://www.veeam.com/
___
## Test Task

Please implement a program that synchronizes two folders: source and replica. The
program should maintain a full, identical copy of source folder at replica folder.
Solve the test task by writing a program in one of these programming languages: **Python, C/C++, C#**

- Synchronization must be one-way: after the synchronization content of the
replica folder should be modified to exactly match content of the source
folder;
- Synchronization should be performed periodically.
- File creation/copying/removal operations should be logged to a file and to the
console output;
- Folder paths, synchronization interval and log file path should be provided
using the command line arguments;
- It is undesirable to use third-party libraries that implement folder
synchronization;
- It is allowed (and recommended) to use external libraries implementing other
well-known algorithms. For example, there is no point in implementing yet
another function that calculates MD5 if you need it for the task – it is
perfectly acceptable to use a third-party (or built-in) library.

___
## Usage
```
Arguments:
  SOURCE    Path to the source folder.
  REPLICA   Path to the replica folder.
  INTERVAL  Synchronization interval in seconds.
  LOGFILE   Path to the log file.

Options:
  -h, --help      Show this help message and exit.
  -v, --version   Show version information and exit.

Example:
  python sync_folders.py /path/to/source /path/to/replica 60 /path/to/logfile.log
```