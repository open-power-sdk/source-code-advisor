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
        * Roberto Oliveira <rdutra@br.ibm.com>
"""

import unittest

from sca.sca_events.sca_xml import *


class ScaXmlTest(unittest.TestCase):
    """ Class to run tests from sca xml """

    def test_load_xml(self):
        sca_xml = ScaXml()
        events = sca_xml.get_event_list()
        assert not [] == events

        # Test with an existing event
        event = next((event for event in events
                      if event.name == "MOVE HOT CODE TO COLD AREA"), None)
        assert not None == event

        expected_problem = "Invariant or infrequently executed code "\
            "found within a loop."
        expected_solution = "\n\tMove the flagged code outside the loop."

        self.assertEqual(expected_problem, event.get_problem())
        self.assertEqual(expected_solution, event.get_solution())

        # Test with a non existing event
        event = next((event for event in events if event.name == "BLA"), None)
        assert None == event


if __name__ == '__main__':
    unittest.main()
