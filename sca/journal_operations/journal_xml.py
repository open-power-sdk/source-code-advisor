# -*- coding: utf-8 -*-
"""
Copyright (C) 2017 IBM Corporation

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
        * Diego Fernandez-Merjildo <merjildo@br.ibm.com>
"""

import xml.etree.ElementTree as elemTree


class Operation(object):
    '''Class to hold operation values which comes from journal file'''
    name = ''
    problem = ''
    solution = ''
    site_dict = {}
    params = []

    def __init__(self, name, problem, solution, site_dict):
        self.name = name
        self.problem = problem
        self.solution = solution
        self.site_dict = site_dict

    def set_site(self, site_dict):
        '''Set site value'''
        self.site_dict = site_dict

    def get_site(self):
        '''Get site value'''
        return self.site_dict

    def get_name(self):
        '''Get operation name'''
        return self.name

    def get_problem(self):
        '''Get problem reported'''
        return self.problem

    def get_solution(self):
        '''Get initial solution'''
        return self.solution


class JournalXml(object):
    '''Class to parse operation that comes from fdpr'''

    def __init__(self):
        self.operation_list = []

    def load_xml(self, file_name):
        '''Function to load Operation from journal file'''
        tree = elemTree.parse(file_name)
        root = tree.getroot()

        for oper in root.iter('operation'):
            site_dict = {'line':  oper.find('site').find('line').text,
                         'dir': oper.find('site').find('dir').text,
                         'file': oper.find('site').find('file').text,
                         'function': oper.find('site').find('fn').text,
                         'address': oper.find('site').find('ip').text}
            operation = Operation(oper.attrib['name'], oper.find('problem').text,
                                  oper.find('solution').text, site_dict)
            self.operation_list.append(operation)

    def get_operation_list(self):
        '''Function to get operation list'''
        return self.operation_list
