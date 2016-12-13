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
import os

from sca.journal_operations.journal_xml import *


class JournalXmlTest(unittest.TestCase):
    """ Class to run tests from journal xml """
    DIR_PATH = os.path.dirname(os.path.realpath("sca"))

    def test_load_xml(self):
        jour_file = self.DIR_PATH + "/tests/fdpr_journal_example.xml"
        journal_xml = JournalXml()
        journal_xml.load_xml(jour_file)
        operations = journal_xml.get_operation_list()
        assert not [] == operations
        self.assertEqual(68, len(operations))

        # Test first operation element
        operation = operations[0]
        self.assertEquals("Toc store in loop optimization",
                          operation.get_name())
        self.assertEquals("high penalty for toc store in loop operation",
                          operation.get_problem())
        self.assertEquals("relocate toc store from loop to before loop",
                          operation.get_solution())

        site = operation.get_site()
        self.assertEquals("103fcfa4", site['address'])
        self.assertEquals("/home/iplsdk/projects/php-src/Zend", site['dir'])
        self.assertEquals("zend_vm_execute.h", site['file'])
        self.assertEquals("execute_ex", site['function'])
        self.assertEquals("414", site['line'])


if __name__ == '__main__':
    unittest.main()
