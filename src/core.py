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

class FileInfo(object):
    '''This class hold file info from Fdpr'''
    def __init__(self, file_name, function, line):
        self.file_name = file_name
        self.function = function
        self.line = line

    def get_file_name(self):
        '''Return file name'''
        return self.file_name

    def get_function(self):
        '''return function problem'''
        return self.function

    def get_line(self):
        '''return line number'''
        return self.line

class Problem(object):
    '''This class contains info about a problem
    reported by fdpr '''
    def __init__(self, name_problem, problem_description, solution):
        self.name_problem = name_problem
        self.problem_description = problem_description
        self.solution = solution
        self.file_info_list = []

    def add_file_info(self, file_info):
        '''Add a new FileInfo object, file info
        about a file with same problem'''
        self.file_info_list.append(file_info)

    def get_file_info_list(self):
        '''returns a list of FileInfo objects'''
        return self.file_info_list

    def get_name_problem(self):
        '''return name problem'''
        return self.name_problem

    def get_problem_description(self):
        ''' return problem description'''
        return self.problem_description

    def get_solution(self):
        '''return solution  of the problem'''
        return self.solution

def show_logo():
    ''' This function shows SCA header '''
    print '''
  ####################################################################
  #                                                                  #
  #                   SDK Tools  - SOURCE CODE ADVISOR               #
  #                                                                  #
  ####################################################################
    '''

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

def print_sca(problems_dict):
    ''' This function shows events info '''
    show_logo()
    if not bool(problems_dict):
        print "SCA : No reports found."
        return

    for key in problems_dict:
        print "[Problem: {}]".format(problems_dict.get(key).get_name_problem())
        print "[Description: {}]".format(problems_dict.get(key).get_problem_description())
        print "     \\"
        print "      [Solution]"
        print problems_dict.get(key).get_solution()
        print ""
        for file_inf in problems_dict[key].get_file_info_list():
            file_name = file_inf.get_file_name()
            line = file_inf.get_line()
            print "     [Source file: %s : %s] " % (line, file_name)
        print "-------------------------------------------------------"
        print ""

def set_group_events(operations, events):
    ''' This function group source files or lines
    in source files with the same problem '''
    problems_dict = {}
    for oper in operations:
        for event in events:
            if event.get_name() == oper.get_name().upper():
                prb_name = event.get_name()
                file_name = oper.get_site().get('dir') +  "/" + oper.get_site().get('file')
                line = linecache.getline(file_name, int(oper.get_site().get('line')))
                file_info = FileInfo(file_name, line.strip(), oper.get_site().get('line'))

                if problems_dict.get(prb_name, None) != None:
                    problems_dict.get(prb_name).get_file_info_list().append(file_info)
                else:
                    problem = Problem(prb_name, event.get_problem(), event.get_solution())
                    problem.add_file_info(file_info)
                    problems_dict[prb_name] = problem

    return problems_dict

def run_xml_match(journal_file):
    ''' This function match events from xml info'''
    journal_xml = JournalXml()
    journal_xml.load_xml(journal_file)
    operations = journal_xml.get_operation_list()

    sca_xml = ScaXml()
    events = sca_xml.get_event_list()

    group_problems = set_group_events(operations, events)
    print_sca(group_problems)
