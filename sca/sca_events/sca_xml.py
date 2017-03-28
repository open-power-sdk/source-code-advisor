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
import os

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
LOCAL_XML_SCA = DIR_PATH + "/sca_events.xml"


class Event(object):
    ''' Class to hold SCA events'''
    name = ''
    problem = ''
    solution = ''
    marker_id = ''

    def __init__(self, name, problem, solution, marker_id):
        self.name = name
        self.problem = problem
        self.solution = solution
        self.marker_id = marker_id

    def get_name(self):
        ''' Function to get event name '''
        return self.name

    def get_problem(self):
        ''' Function to get problem description'''
        return self.problem

    def get_solution(self):
        ''' Function to get solution description'''
        return self.solution

    def get_marker_id(self):
        '''Function to get marker'''
        return self.marker_id


class ScaXml(object):
    ''' Class to parse SCA events'''
    event_list = []

    def __init__(self):
        self.load_xml(LOCAL_XML_SCA)

    def load_xml(self, file_name):
        '''Function to load SCA events'''
        tree = elemTree.parse(file_name)
        root = tree.getroot()
        for evnt in root.iter('event'):
            event = Event(evnt.attrib['name'], evnt.attrib['problem'],
                          evnt.attrib['solution'], evnt.attrib['marker_id'])
            self.event_list.append(event)

    def get_event_list(self):
        '''Function to get SCA events list'''
        return self.event_list
