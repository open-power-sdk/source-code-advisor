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
"""

import unittest
import os

from sca import core


class CoreTests(unittest.TestCase):
    """ Class to run tests from core """

    def test_execute(self):
        self.assertEqual(0, core.execute("ls"))
        self.assertNotEqual(0, core.execute("foo_bar"))

    def test_cmdexist(self):
        assert True == core.cmdexists("cd")
        assert False == core.cmdexists("foo_bar")

    def test_run_xml_match(self):
        """ Test the run_xml_match function and also the set_group_events() """
        dir_path = os.path.dirname(os.path.realpath("sca"))
        jour_file = dir_path + "/tests/fdpr_journal_example.xml"
        problems = core.run_xml_match(jour_file)
        self.assertEquals(6, len(problems))

        # Test unroll loop entry
        unroll_loop = problems['UNROLL LOOP']
        self.assertEquals("High branch penalty in a small loop.",
                          unroll_loop.get_problem_description())
        self.assertIn("Specify the GNU extension \"__attribute__ ((optimize",
                      unroll_loop.get_solution())

        # All unroll loop problems
        unroll_problems = unroll_loop.get_file_info_list()
        self.assertEquals(10, len(unroll_problems))


if __name__ == '__main__':
    unittest.main()
