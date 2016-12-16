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
import json
from colorclass import Color
from sca_events import ScaXml
from journal_operations import JournalXml

DIR_PATH = os.path.dirname(os.path.realpath(__file__))


class FileInfo(object):
    '''This class hold file info from Fdpr'''
    def __init__(self, file_name, function, line, address):
        self.file_name = file_name
        self.function = function
        self.line = line
        self.address = address

    def get_file_name(self):
        '''Return file name'''
        return self.file_name

    def get_function(self):
        '''return function problem'''
        return self.function

    def get_line(self):
        '''return line number'''
        return self.line

    def get_address(self):
        """ return adress (ip) """
        return self.address


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


def print_output(msg_type, flag, msg):
    """ SCA print function, enables color usage """
    color_open = ''
    color_close = ''

    if flag:
        if msg_type == 'ERROR':
            color_open = "{hired}"
            color_close = "{/hired}"

        if msg_type == 'INFO':
            color_open = "{higreen}"
            color_close = "{/higreen}"

        if msg_type == 'WARNING':
            color_open = "{hiyellow}"
            color_close = "{/hiyellow}"

    print Color(color_open + msg + color_close)


def print_sca(problems_dict, color_flag):
    ''' This function shows events info '''
    for key in problems_dict:
        problem = problems_dict.get(key)
        msg_problem = "\n[Problem: {}]".format(problem.get_name_problem())
        print_output('ERROR', color_flag, msg_problem)

        msg_descript = "[Description: {}]".format(problem.get_problem_description())
        print_output('ERROR', color_flag, msg_descript)

        print_output('INFO', color_flag, "[Solution:")
        print_output('INFO', color_flag, problem.get_solution())

        for file_inf in problems_dict[key].get_file_info_list():
            file_name = file_inf.get_file_name()
            line = file_inf.get_line()
            function_name = file_inf.get_function()
            address = file_inf.get_address()

            # Dont show if dont have line number information
            reference = ""
            if line != "0":
                reference = "Reference: %s:%s | " % (file_name, line)
            function = "Function: %s" % (function_name)
            ip_add = "Instruction Pointer: %s" % (address)

            msg_ref = "[%s%s | %s] " % (reference, function, ip_add)
            print_output('WARNING', color_flag, msg_ref)
        print "-------------------------------------------------------"


def save_sca_txt(problems_dict, file_name):
    ''' This function saves events info in a txt file'''
    with open(file_name, 'w') as output_file:
        for key in problems_dict:
            problem = problems_dict.get(key)
            output_file.write("[Problem: {}]\n".format(
                problem.get_name_problem()))
            output_file.write("[Description: {}]\n".format(
                problem.get_problem_description()))

            output_file.write("[Solution:\n")
            output_file.write(problem.get_solution() + "\n]")
            output_file.write("\n")
            for file_inf in problems_dict[key].get_file_info_list():
                file_name = file_inf.get_file_name()
                line = file_inf.get_line()
                function_name = file_inf.get_function()
                address = file_inf.get_address()

                # Dont show if dont have line number information
                reference = ""
                if line != "0":
                    reference = "Reference: %s:%s | " % (file_name, line)
                function = "Function: %s" % (function_name)
                ip_address = "Instruction Pointer: %s" % (address)

                output_file.write("[%s%s | %s] \n" % (reference, function,
                                                      ip_address))
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
                function = oper.get_site().get('function')
                line = oper.get_site().get('line')
                address = oper.get_site().get('address')
                file_info = FileInfo(file_path, function, line, address)

                if problems_dict.get(prb_name, None) is not None:
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
