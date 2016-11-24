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

def run_sca(binary_path, binary_args, sca_options):
    '''Run the SCA tool'''
    if not core.cmdexists(FDPRPRO):
        sys.stderr.write("fdprpro package is not installed. Install it and and try again.\n")
        sys.exit(0)
    elif not core.cmdexists(FDPR_WRAP):
        sys.stderr.write("fdpr_wrap package is not installed. Install it and try again.\n")
        sys.exit(0)
    else:
        # Export fdpr flags in system environment
        os.environ['FDPR_OPT_FLAGS'] = sca_options.get_fdpr_opt()

        # Get binary absolute path
        binary_path = os.path.realpath(binary_path)

        status = core.execute(FDPR_WRAP + " " + binary_path + " " + binary_args)
        check_exit_status(status)

        jour_file = binary_path + "-jour.xml"
        group_problems = core.run_xml_match(jour_file)

        if sca_options.get_file_type_opt() == 'txt':
            core.save_sca_txt(group_problems, sca_options.get_file_name())
        else:
            core.print_sca(group_problems)

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
