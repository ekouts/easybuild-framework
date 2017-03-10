##
# Copyright 2016-2017 Ghent University
#
# This file is part of EasyBuild,
# originally created by the HPC team of Ghent University (http://ugent.be/hpc/en),
# with support of Ghent University (http://ugent.be/hpc),
# the Flemish Supercomputer Centre (VSC) (https://vscentrum.be/nl/en),
# Flemish Research Foundation (FWO) (http://www.fwo.be/en)
# and the Department of Economy, Science and Innovation (EWI) (http://www.ewi-vlaanderen.be/en).
#
# http://github.com/hpcugent/easybuild
#
# EasyBuild is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation v2.
#
# EasyBuild is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EasyBuild.  If not, see <http://www.gnu.org/licenses/>.
##
"""
Style tests for easyconfig files.

:author: Ward Poelmans (Ghent University)
"""

import glob
import os
import sys
from test.framework.utilities import EnhancedTestCase, TestLoaderFiltered
from unittest import TextTestRunner
from vsc.utils import fancylogger
from easybuild.framework.easyconfig.style import _eb_check_trailing_whitespace, check_easyconfigs_style

try:
    import pep8
except ImportError:
    pass


class StyleTest(EnhancedTestCase):
    log = fancylogger.getLogger("StyleTest", fname=False)

    def test_style_conformance(self):
        """Check the easyconfigs for style"""
        if 'pep8' not in sys.modules:
            print "Skipping style checks (no pep8 available)"
            return

        # all available easyconfig files
        test_easyconfigs_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'easyconfigs', 'test_ecs')
        specs = glob.glob('%s/*.eb' % test_easyconfigs_path)
        specs = sorted(specs)

        result = check_easyconfigs_style(specs)

        self.assertEqual(result, 0, "No code style errors (and/or warnings) found.")

    def test_check_trailing_whitespace(self):
        """Test for trailing whitespace check."""
        lines = [
            "name = 'foo'",  # no trailing whitespace
            "version = '1.2.3'  ",  # trailing whitespace
            "   ",  # blank line with whitespace included
            '''description = """start of long description, ''',  # trailing whitespace, but allowed in description
            ''' continuation of long description ''',  # trailing whitespace, but allowed in continued description
            ''' end of long description"""''',
            "moduleclass = 'tools'   ",  # trailing whitespace
            '',
        ]
        line_numbers = range(1, len(lines) + 1)
        test_cases = [
            ({}, None),
            ({}, (17, "W299 trailing whitespace")),
            ({}, (0, "W293 blank line contains whitespace")),
            ({}, None),
            ({'eb_last_key': 'description'}, None),
            ({'eb_last_key': 'description'}, None),
            ({'eb_last_key': 'description'}, (21, "W299 trailing whitespace")),
        ]

        for (line, line_number, (checker_state, expected_result)) in zip(lines, line_numbers, test_cases):
            result = _eb_check_trailing_whitespace(line, lines, line_number, checker_state)
            self.assertEqual(result, expected_result)


def suite():
    """Return all style tests for easyconfigs."""
    return TestLoaderFiltered().loadTestsFromTestCase(StyleTest, sys.argv[1:])


if __name__ == '__main__':
    TextTestRunner(verbosity=1).run(suite())
