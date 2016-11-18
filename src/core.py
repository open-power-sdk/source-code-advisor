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
		* Roberto Oliveira <rdutra@br.ibm.com>
		* Diego Fernandez-Merjildo <merjildo@br.ibm.com>
"""

import subprocess
import os
import linecache
from sca_events import ScaXml
from journal_operations import JournalXml

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
COLOR_HEADER = '\033[95m'
COLOR_OKBLUE = '\033[94m'
COLOR_OKGREEN = '\033[92m'
COLOR_WARNING = '\033[93m'
COLOR_FAIL = '\033[91m'
COLOR_ENDC = '\033[0m'
COLOR_BOLD = '\033[1m'
COLOR_UNDERLINE = '\033[4m'


def show_logo():
    ''' This function shows SCA header '''
    print COLOR_HEADER + '''
  ####################################################################
  #                                                                  #
  #                   SDK Tools  - SOURCE CODE ADVISOR               #
  #                                                                  #
  ####################################################################
    ''' + COLOR_ENDC

def execute(command):
    """execute a command with its parameters"""
    try:
        return subprocess.check_call([command], stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as excp:
        return excp.returncode

def cmdexists(command):
    """check if a command exists"""
    subp = subprocess.call("type " + command, shell=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return subp == 0

def print_code_advisor(operations, events):
    ''' This function shows events info '''
    for oper in operations:
        file_name = oper.get_site().get('dir') +  "/" + oper.get_site().get('file')
        line = linecache.getline(file_name, int(oper.get_site().get('line')))
        print COLOR_FAIL + ("  [Source file: %s] " % file_name) + COLOR_ENDC
        print COLOR_FAIL + ("  [Problem: {} ]".format(oper.get_problem())) + COLOR_ENDC
        print COLOR_WARNING + ("  [Function: {}  line: {}]".format(line.strip(),
                                                                   oper.get_site().get('line'))
                              ) + COLOR_ENDC
        print "     \\"

        for event in events:
            if event.get_name() == oper.get_name().upper():
                print COLOR_OKBLUE + "      [Solution]" + COLOR_ENDC
                print event.get_solution()
                print ""


def run_xml_match(journal_file):
    ''' This function match events from xml info'''
    journal_xml = JournalXml()
    journal_xml.load_xml(journal_file)
    operations = journal_xml.get_operation_list()

    sca_xml = ScaXml()
    events = sca_xml.get_event_list()

    show_logo()
    print_code_advisor(operations, events)
