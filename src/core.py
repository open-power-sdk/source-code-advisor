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

class ScaColor(object):
    ''' Class to hold colors '''
    def __init__(self, flag):
        self.header = ''
        self.okblue = ''
        self.okgreen = ''
        self.warning = ''
        self.fail = ''
        self.endc = ''
        self.bold = ''
        self.underline = ''

        if flag:
            self.with_color()

    def with_color(self):
        '''Set colors values'''
        self.header = '\033[95m'
        self.okblue = '\033[94m'
        self.okgreen = '\033[92m'
        self.warning = '\033[93m'
        self.fail = '\033[91m'
        self.endc = '\033[0m'
        self.bold = '\033[1m'
        self.underline = '\033[4m'

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

def print_sca(problems_dict, color_flag):
    ''' This function shows events info '''
    col = ScaColor(color_flag)
    print col.header
    show_logo()
    print col.endc
    if not bool(problems_dict):
        print col.warning + "SCA : No reports found." + col.endc
        return

    for key in problems_dict:
        print col.fail + "[Problem: {}]".format(problems_dict.get(key).get_name_problem())
        print "[Description: {}]".format(
            problems_dict.get(key).get_problem_description()) + col.endc + col.okgreen
        print "     \\"
        print "      [Solution]"
        print problems_dict.get(key).get_solution()
        print col.endc
        print ""
        for file_inf in problems_dict[key].get_file_info_list():
            file_name = file_inf.get_file_name()
            line = file_inf.get_line()
            print col.warning + "     [Source file: %s : %s] " % (file_name, line) + col.endc
        print "-------------------------------------------------------"
        print ""

def save_sca_txt(problems_dict, file_name):
    ''' This function saves events info in a txt file'''
    with open(file_name, 'w') as output_file:
        output_file.write(" ####################################################################\n")
        output_file.write(" #                                                                  #\n")
        output_file.write(" #                   SDK Tools  - SOURCE CODE ADVISOR               #\n")
        output_file.write(" #                                                                  #\n")
        output_file.write(" ####################################################################\n")
        output_file.write(" \n")

        if not bool(problems_dict):
            output_file.write("SCA : No reports found.")
        else:
            for key in problems_dict:
                output_file.write("[Problem: {}]\n".format(
                    problems_dict.get(key).get_name_problem()))
                output_file.write("[Description: {}]\n".format(
                    problems_dict.get(key).get_problem_description()))
                output_file.write("     \\ \n")
                output_file.write("      [Solution]\n")
                output_file.write(problems_dict.get(key).get_solution())
                output_file.write("\n\n")

                for file_inf in problems_dict[key].get_file_info_list():
                    file_name_src = file_inf.get_file_name()
                    line = file_inf.get_line()
                    output_file.write("     [Source file: %s : %s] \n" % (file_name_src, line))

                output_file.write("\n-------------------------------------------------------")
                output_file.write("\n")

    print "\nSCA report was saved on file: " + file_name

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
    return group_problems
