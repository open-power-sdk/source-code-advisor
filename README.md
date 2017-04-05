# Project Description
Report potential performance issues and possible remedies for a given
executable.

SCA will non-destructively instrument the executable and run the
instrumented version, collecting performance data. Upon completion,
a report will be presented listing any detected issues with possible
remedies.

IMPORTANT: To use SCA the binary must be linked with relocation
information preserved, which is not the default linker behavior.
Add "-q" or "--preserve-relocs" to the "ld" command or "-Wl,-q"
or "-Wl,--preserve-relocs" if the compiler is used to link."

Source Code Advisor (SCA) and Feedback-Directed Program Restructuring (FDPR)
work together to allow you to analyze and optimize your applications.

FDPR works similarly to a compiler: it reads a linked executable program and
produces an optimized version of it. Both regular executable and shared library
forms are supported. The optimization uses an execution profile, collected by
running an instrumented version of the input.

During the code optimization process, FDPR produces a journal of the optimizations
performed. The Source Code Advisor uses this journal, produced as an XML file,
to highlight potential problems in your source code and to offer suggested solutions.
The journal explains each optimization site, including the source location,
execution count, the performance problem found, and the user action required to
resolve the problem. It is important to select a representative workload for
both SCA and for FDPR so that the optimization step is effective.

Because SCA uses information gathered by FDPR, knowledge of this tool is important.

The combination of SCA and FDPR provide you with two major approaches to performance
analysis and optimization:

* Find and visualize performance problems in the source program using feedback-directed analysis.

* Perform feedback-directed optimization of an executable program (or a shared library).

For more information about SCA usage, see sca --help

## Contributing to the project
We welcome contributions to the Source Code Advisor Project in many forms. There's always plenty to do! Full details of how to contribute to this project are documented in the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## Maintainers
The project's [maintainers](MAINTAINERS.txt): are responsible for reviewing and merging all pull requests and they guide the over-all technical direction of the project.

## Communication <a name="communication"></a>
We use [Slack](https://toolsforpower.slack.org/) for communication.

## Supported Architecture and Operating Systems

ppc64le: Ubuntu 16.04, CentOS7, RHEL 7.3, Fedora 25.

## Installing

Requirements: python-pip, python-pylint, python-virtualenv, python-docsutil, fdprpro and fdprwrap

Testing: ./dev tests

Build: ./dev release

Build and install: ./dev install

Execution: sca --help

## FDPRPro and FDPRWrap

Both are proprietary tools by IBM which are freely available at https://developer.ibm.com/linuxonpower/sdk-packages/. Ensure you have both tools installed in order to execute Source Code Advisor.

## Documentation

usage: sca [-h] [--version] [--color] [--fdprpro-args [FDPRPRO_ARGS]]
           [--output-type [{txt,json}]] [--output-name [FILE_NAME]]
           COMMAND

COMMAND    the application and its arguments
           e.g.: sca <command>

-h, --help  show this help message and exit

--version, -V   show program's version number and exit

--color  displays results in color

--fdprpro-args [FDPRPRO_ARGS]
                fdprpro options
                e.g.: --fdprpro-args='-O3 -v 3'
                To get all available options for fdprpro issue:
                /opt/ibm/fdprpro/bin/fdprpro --help

--output-type [{txt,json}]
                The output of the report file
                e.g.:--output-type=txt

--output-name [FILE_NAME]
                The name of the report file
                e.g.: --output-name=file_name

## Still Have Questions?
For general purpose questions, please use [StackOverflow](http://stackoverflow.com/questions/tagged/toolsforpower).

## License <a name="license"></a>
The Source Code Advisor Project uses the [Apache License Version 2.0](LICENSE) software license.

## Related information
[FDPR] (https://www.research.ibm.com/haifa/projects/systems/cot/fdpr/)



























Source Code Advisor - SCA
=========================




Supported Architecture and Operating Systems
=========================

* ppc64le: Ubuntu 16.04, CentOS7, RHEL 7.3, Fedora 25.


Building and Testing
=========================

Requirements: python-pip, python-pylint, python-virtualenv, python-docsutil, fdprpro and fdprwrap

Testing: ./dev tests

Build: ./dev release

Build and install: ./dev install


FDPRPro and FDPRWrap
=========================

Both are proprietary tools by IBM which are freely available at https://developer.ibm.com/linuxonpower/sdk-packages/. Ensure you have both tools installed in order to execute Source Code Advisor.


Integrators
=========================

If you intend to integrate SCA within your development environemt you should be aware of the following error codes:

0: no problems occurred

1: generic error code.

2: some dependency tool is missing
