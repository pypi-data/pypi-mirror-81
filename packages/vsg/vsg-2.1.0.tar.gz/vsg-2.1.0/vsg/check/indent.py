'''
This module contains functions for rules to perform their checks.
'''

import re

from vsg import utils


def indent(self, oLine, iLineNumber):
    '''
    Adds a violation if the indent of the line does not match the desired level.

    Parameters

      self: (rule object)

      oLine: (line object)

      iLineNumber: (integer)

    '''
    if not oLine.isBlank:
        try:
            if not re.match('^\s{' + str(self.indentSize * oLine.indentLevel) + '}\S', oLine.line):
                self.add_violation(utils.create_violation_dict(iLineNumber))
        except TypeError:
            pass
