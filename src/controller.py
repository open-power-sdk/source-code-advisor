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
"""

import core
import sys

FDPR='/opt/ibm/fdprpro/bin/fdprpro'

def runsca(binary_path, binary_name, opt_value, warn_value, verbose_value, processor_value):
	if [core.cmdexists(FDPR)]:
		core.execute(FDPR + " -a instr -p " + binary_path + " -w " + str(warn_value) + " -v " + str(verbose_value) + " -f ./" + binary_name + ".prof -fd 999 -o " + binary_name + ".instr")
		core.execute(binary_path)
		core.execute(FDPR + " -a opt -O" + str(opt_value) + " -w " + str(warn_value) + " -v " + str(verbose_value) + " -m " + processor_value + " -p " + binary_path + " -f ./" + binary_name +".prof -o ./" + binary_name + ".fdpr.opt -j " + binary_name + ".xml")
	else:
		sys.stderr.write("FDPR is not installed. Fix it and try again.")
		sys.exit(0)
