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
import json
from sca_events import ScaXml
from journal_operations import JournalXml

DIR_PATH = os.path.dirname(os.path.realpath(__file__))


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

    def to_json(self):
        '''This function implements serialization'''
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

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


def get_sca_color(flag):
    '''Set colors values'''
    col_dict = {}
    col_dict['header'] = ''
    col_dict['okblue'] = ''
    col_dict['okgreen'] = ''
    col_dict['warning'] = ''
    col_dict['fail'] = ''
    col_dict['endc'] = ''
    col_dict['bold'] = ''
    col_dict['underline'] = ''

    if flag:
        col_dict['header'] = '\033[95m'
        col_dict['okblue'] = '\033[94m'
        col_dict['okgreen'] = '\033[92m'
        col_dict['warning'] = '\033[93m'
        col_dict['fail'] = '\033[91m'
        col_dict['endc'] = '\033[0m'
        col_dict['bold'] = '\033[1m'
        col_dict['underline'] = '\033[4m'

    return col_dict


def print_sca(problems_dict, color_flag):
    ''' This function shows events info '''
    col = get_sca_color(color_flag)
    print col['header']
    print col['endc']
    if not bool(problems_dict):
        print col['warning'] + "SCA : No reports found." + col['endc']
        return

    for key in problems_dict:
        print col['fail'] + "[Problem: {}]".format(problems_dict.get(key).get_name_problem())
        print "[Description: {}]".format(
            problems_dict.get(key).get_problem_description()) + col['endc'] + col['okgreen']
        print "[Solution:"
        print problems_dict.get(key).get_solution() + "]"
        print col['endc']
        print ""
        for file_inf in problems_dict[key].get_file_info_list():
            file_name = file_inf.get_file_name()
            line = file_inf.get_line()
            print col['warning'] + "[Source file: %s : %s] " % (file_name, line) + col['endc']
        print "-------------------------------------------------------"
        print ""


def save_sca_txt(problems_dict, file_name):
    ''' This function saves events info in a txt file'''
    with open(file_name, 'w') as output_file:
        if not bool(problems_dict):
            output_file.write("SCA : No reports found.")
        else:
            for key in problems_dict:
                output_file.write("[Problem: {}]\n".format(
                    problems_dict.get(key).get_name_problem()))
                output_file.write("[Description: {}]\n".format(
                    problems_dict.get(key).get_problem_description()))
                output_file.write("[Solution:\n")
                output_file.write(problems_dict.get(key).get_solution()) + "]"
                output_file.write("\n\n")
                for file_inf in problems_dict[key].get_file_info_list():
                    file_name_src = file_inf.get_file_name()
                    line = file_inf.get_line()
                    output_file.write("[Source file: %s : %s] \n" % (file_name_src, line))
                output_file.write("\n-------------------------------------------------------")
                output_file.write("\n")


def save_sca_json(problems_dict, file_name):
    '''This function saves events info in a Json file'''
    with open(file_name, 'w') as outfile:
        for key in problems_dict:
            outfile.write(problems_dict.get(key).to_json())


def save_sca(problems_dict, file_name, file_type):
    '''This function saves events in a file'''
    ret_val = False
    if file_type == 'txt':
        save_sca_txt(problems_dict, file_name)
        ret_val = True
    elif file_type == 'json':
        save_sca_json(problems_dict, file_name)
        ret_val = True

    return ret_val


def set_group_events(operations, events):
    ''' This function group source files or lines
    in source files with the same problem '''
    problems_dict = {}
    for oper in operations:
        for event in events:
            if event.get_name() == oper.get_name().upper():
                prb_name = event.get_name()
                file_name = oper.get_site().get('file') or ''
                file_path = oper.get_site().get('dir') + "/" + file_name
                line = linecache.getline(file_path, int(oper.get_site().get('line')))
                file_info = FileInfo(file_path, line.strip(), oper.get_site().get('line'))

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
