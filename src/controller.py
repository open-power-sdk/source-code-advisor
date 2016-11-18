# -*- coding: utf-8 -*-

"""
Copyright (C) 2016 IBM Corporation

Licensed under the Apache License, Version 2.0 (the “License”);
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an “AS IS” BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

	Contributors:
		* Rafael Sene <rpsene@br.ibm.com>
		* Diego Fernandez-Merjildo <merijldo@br.ibm.com>
        * Roberto Oliveira <rdutra@br.ibm.com>
"""

import sys
import os
import core

FDPRPRO = '/opt/ibm/fdprpro/bin/fdprpro'
FDPR_WRAP = '/opt/ibm/fdprpro/bin/fdpr_instr_prof_jour'

def run_sca(binary_cmd, binary_name, options):
    '''Run the SCA tool'''
    opt_value = options.get_opt()
    warn_value = options.get_warn()
    verbose_value = options.get_verbose()
    processor_value = options.get_proc()

    if not core.cmdexists(FDPRPRO):
        sys.stderr.write("fdprpro package is not installed. Install it and and try again.\n")
        sys.exit(0)
    elif not core.cmdexists(FDPR_WRAP):
        sys.stderr.write("fdpr_wrap package is not installed. Install it and try again.\n")
        sys.exit(0)
    else:
        # Available optimization levels in FDPR: O, O2, O3, O4
        if opt_value == '1':
            opt_value = ''

        # Create flags to be passed to fdpr
        opt_flag = "-O" + str(opt_value)
        warn_flag = "-w " + str(warn_value)
        verbose_flag = "-v " + str(verbose_value)
        processor_flag = "-m " + processor_value

        # Export flags in system environment
        cmd = ''
        cmd += opt_flag + " "
        cmd += warn_flag + " "
        cmd += verbose_flag + " "
        cmd += processor_flag
        os.environ['FDPR_OPT_FLAGS'] = cmd

        status = core.execute(FDPR_WRAP + " " + binary_cmd)
        check_exit_status(status)

        jour_file = binary_name + "-jour.xml"
        core.run_xml_match(jour_file)

def check_exit_status(status):
    """
    Check execution exit status
    """
    if status == 1:
        sys.stderr.write('FDPR failed during application instrumentation.\n')
        sys.exit(0)
    elif status == 2:
        sys.stderr.write('FDPR failed during application profiling.\n')
        sys.exit(0)
    elif status == 3:
        sys.stderr.write('FDPR failed during journal production.\n')
        sys.exit(0)
