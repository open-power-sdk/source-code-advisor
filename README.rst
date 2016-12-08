Source Code Advisor - SCA
=========================

Source Code Advisor (SCA) and Feedback-Directed Program Restructuring (FDPR) work together to
allow you to analyze and optimize your applications.

FDPR works similarly to a compiler: it reads a linked executable program and produces an optimized
version of it. Both regular executable and shared library forms are supported. The optimization uses an
execution profile, collected by running an instrumented version of the input.

During the code optimization process, FDPR produces a journal of the optimizations performed. The
Source Code Advisor uses this journal, produced as an XML file, to highlight potential problems in your
source code and to offer suggested solutions. The journal explains each optimization site, including the
source location, execution count, the performance problem found, and the user action required to resolve
the problem. It is important to select a representative workload for both SCA and for FDPR so that the
optimization step is effective.

Because SCA uses information gathered by FDPR, knowledge of this tool is important.

The combination of SCA and FDPR provide you with two major approaches to performance analysis and
optimization:
        * Find and visualize performance problems in the source program using feedback-directed analysis.
        * Perform feedback-directed optimization of an executable program (or a shared library).

--------------------------------------------------------------------------------------------------------

Usage: sca [-h] [--version] [--color] [--fdprpro-args [FDPRPRO_ARGS]]
           [--output-type [{txt,json}]] [--output-name [FILE_NAME]]
           application_path [application_path ...]


positional arguments:
  application_path      path to the application binary and its arguments

optional arguments:
  -h, --help            show this help message and exit
  --version, -V         show program's version number and exit
  --color               displays results in color
  --fdprpro-args [FDPRPRO_ARGS]
                        fdprpro options, e.g.: --fdprpro-args='-O3 -v 3'. To
                        get all available options for fdprpro issue:
                        /opt/ibm/fdprpro/bin/fdprpro --help
  --output-type [{txt,json}]
                        The output of the report file. e.g.:--output-type=txt
  --output-name [FILE_NAME]
                        The name of the report file. e.g.: --output-
                        name=file_name


Exit Status
    SCA may return one of several error codes if it encounters problems.

    0 No problems occurred.
    1 Generic error code.
    2 Some dependency tool is missing.
