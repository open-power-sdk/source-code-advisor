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
        * Rafael Peria de Sene <rpsene@br.ibm.com>
        * Diego Fernandez-Merjildo <merjildo@br.ibm.com>
        * Roberto Oliveira <rdutra@br.ibm.com>
        """

import sys
import os
import argparse

from argparse import ArgumentParser
from argparse import RawTextHelpFormatter
import pkg_resources
import controller


__all__ = []
__version__ = pkg_resources.require("sca")[0].version


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

    program_version = "v%s" % __version__
    program_version_message = '%%(prog)s %s' % (program_version)
    program_shortdesc = '''
    --- Source Code Advisor (SCA) ---
    Report potential performance issues and possible remedies for a given
    executable.

    SCA will non-destructively instrument the executable and run the
    instrumented version, collecting performance data. Upon completion,
    a report will be presented listing any detected issues with possible
    remedies.

    IMPORTANT: To use SCA the binary must be linked with relocation
    information preserved, which is not the default linker behavior.
    Add "-q" or "--preserve-relocs" to the "ld" command or "-Wl,-q"
    or "-Wl,--preserve-relocs" if the compiler is used to link."
    '''

    try:
        parser = ArgumentParser(description=program_shortdesc,
                                formatter_class=RawTextHelpFormatter)
        parser.add_argument('--version', '-V', action='version',
                            version=program_version_message)
        parser.add_argument("--fdprpro-args", dest="fdprpro_args", type=str,
                            help="fdprpro options \n"
                            "e.g.: --fdprpro-args='-O3 -v 3'\n"
                            "To get all available options for fdprpro issue:\n"
                            "/opt/ibm/fdprpro/bin/fdprpro --help\n\n",
                            default='', nargs='?')
        parser.add_argument("--output-type", dest="file_type", type=str,
                            help="The output of the report file\n"
                            "e.g.:--output-type=txt\n\n",
                            default=None, choices=['txt', 'json'],
                            nargs='?')
        group = parser.add_mutually_exclusive_group()
        group.add_argument("--output-name", dest="file_name", type=str,
                            help="The name of the report file\n"
                            "e.g.: --output-name=file_name\n\n",
                            default=None,
                            nargs='?')
        group.add_argument('--color', dest="color", action='store_true',
                            help="displays results in color\n\n")
        parser.add_argument(dest="cmd",
                            metavar="COMMAND",
                            help="the application and its arguments\n"
                            "e.g.: sca <command>\n\n",
                            nargs=1)
        parser.add_argument(dest="cmd_args",
                            default=None,
                            nargs=argparse.REMAINDER,
                            help=argparse.SUPPRESS)

        # Process arguments
        args = parser.parse_args()
        binary_path = args.cmd[0]
        binary_args = ' '.join(("'" + i + "'") for i in args.cmd_args)
        sca_options = ScaOptions(args.fdprpro_args)
        sca_options.set_color_opt(args.color)

        if args.file_type is not None:
            if args.file_type not in ('txt', 'json'):
                print "File type not supported"
                return
            if args.file_type == 'json' and args.color:
                print "JSON output does not support --color"
		return
            sca_options.set_file_type_opt(args.file_type)
            if args.file_name is not None:
                sca_options.set_file_name(args.file_name)
        elif args.file_name is not None:
            if not args.file_name:
                print "Please set a file name"
                return
            sca_options.set_file_type_opt('txt')

        # Run SCA
        controller.run_sca(binary_path, binary_args, sca_options)
    except KeyboardInterrupt:
        return 1


if __name__ == "__main__":
    sys.exit(main())
