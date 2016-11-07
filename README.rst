Source Code Advisor - SCA
========================

The SCA configuration allows you to specify the workload needed to collect the profile of the program.
When running this configuration, the program is built, if necessary, using the standard project build
process. Once the executable is available, FDPR creates an instrumented version and runs it using the
specified workload. FDPR then performs a pseudo optimization step producing a journal of the
performance problems found. The result is an XML-formatted file that lists the specific problems found,
their exact location in the source, and so on. With the XML journal available, the Source Code Advisor
view is displayed to visualize the set of problems, allowing you to navigate through the problems and
the corresponding places in the source where they were found. The view provides a recommended course
of action for each problem at various abstraction levels (source change, compiler switches, and so on.)
