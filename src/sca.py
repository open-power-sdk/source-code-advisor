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
        * Diego Fernandez-Merjildo <merjildo@br.ibm.com>
        * Roberto Oliveira <rdutra@br.ibm.com>
        """

import sys
import os
import time

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
import controller

__all__ = []
#TODO: these values must be static
__version__ = '1.0.' + time.strftime("%Y%m%d%H%M%S")
__updated__ = time.strftime("%Y/%m/%d|%H:%M:%S")

class CLIError(Exception):
    ''' Command Line error class '''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg

class ScaOptions(object):
    ''' Hold SCA options '''
    def __init__(self, fdpr_opt):
        self.fdpr_opt = fdpr_opt
        self.file_type_opt = None
        self.file_name_opt = None
        self.color_opt = None

    def get_fdpr_opt(self):
        '''return fdpr options'''
        return self.fdpr_opt
    def get_file_type_opt(self):
        ''' Return file type option'''
        return self.file_type_opt
    def get_file_name(self):
        ''' Return file name'''
        return self.file_name_opt
    def get_color_opt(self):
        ''' Return color option'''
        return self.color_opt

    def set_file_type_opt(self, file_type_opt):
        ''' Set file type option'''
        self.file_type_opt = file_type_opt
    def set_file_name(self, file_name_opt):
        ''' Set file name option'''
        self.file_name_opt = file_name_opt
    def set_color_opt(self, color_opt):
        ''' Set color option'''
        self.color_opt = color_opt


def main(argv=None):
    ''' SCA main function '''
    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = '''
    --- Source Code Advisor (SCA) ---
    Report potential performance issues and possible remedies for a given
    executable.

    SCA will non-destructively instrument the executable and run the
    instrumented version, collecting performance data. Upon completion,
    a report will be presented listing any detected issues with possible
    remedies. '''

    program_license = '''%s

    Copyright (C) 2016 IBM Corporation

    Licensed under the Apache License, Version 2.0 (the “License”);
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing,
    software distributed under the License is distributed on an
    “AS IS” BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
    either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

        Contributors:
            * Rafael Sene <rpsene@br.ibm.com>
            * Diego Fernandez-Merjildo <merjildo@br.ibm.com>
            * Roberto Oliveira <rdutra@br.ibm.com>
            ----------------------------------------------------------
            ''' % (program_shortdesc)

    try:
        parser = ArgumentParser(description=program_license,
                                formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument('-V', '--version', action='version', version=program_version_message)

        parser.add_argument("--fdpr-args", dest="fdpr_args", type=str,
                            help="fdprpro options. e.g.: --fdpr-args='-O3 -v 3'", default='',
                            nargs='?')
        parser.add_argument("--file-type", dest="file_type", type=str,
                            help="Save to file options. e.g.: --file-type=txt",
                            default=None, choices=['txt'],
                            nargs='?')
        parser.add_argument("--file-name", dest="file_name", type=str,
                            help="Save to file options. e.g.: --file-name=file_name",
                            default=None,
                            nargs='?')
        parser.add_argument(dest="path", help="path to the application binary",
                            nargs='+')

        # Process arguments
        args, application_args = parser.parse_known_args()
        binary_path = args.path.pop(0)
        binary_args = ' ' + ' '.join(map(str, args.path))
        binary_args = binary_args + ' ' + ' '.join(map(str, application_args))
        sca_options = ScaOptions(args.fdpr_args)

        if args.file_type != None:
            if not args.file_type in ('txt', 'json'):
                print "File type not supported"
                return
            sca_options.set_file_type_opt(args.file_type)
            if args.file_name != None:
                sca_options.set_file_name(args.file_name)
            else:
                sca_options.set_file_name('sca_report' + '.' + args.file_type)
        elif args.file_name != None:
            if not args.file_name:
                print "Please set a file name"
                return
            sca_options.set_file_type_opt('txt')
            sca_options.set_file_name(args.file_name + '.' + sca_options.get_file_type_opt())

        #Run SCA
        controller.run_sca(binary_path, binary_args, sca_options)

    except KeyboardInterrupt:
        return 0
    except Exception, excp:
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(excp) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

if __name__ == "__main__":
    sys.exit(main())
