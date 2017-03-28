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
