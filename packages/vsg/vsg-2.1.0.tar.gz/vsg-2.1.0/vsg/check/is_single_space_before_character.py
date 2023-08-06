'''
This module contains functions for rules to perform their checks.
'''

import re

from vsg import utils


def is_single_space_before_character(self, sCharacter, oLine, iLineNumber):
    '''
    Checks if a single space exists before a series of characters.
    NOTE:  The characters will match partial words.

    Parameters:

      self: (rule object)

      sCharacter: (string)

      oLine: (line object)

      iLineNumber: (integer)
    '''
    iIndex = oLine.line.find(sCharacter) + len(sCharacter)
    if sCharacter in oLine.lineLower:
        if not re.match('^.*\s' + sCharacter.lower(), oLine.lineNoComment[:iIndex]):
            self.add_violation(utils.create_violation_dict(iLineNumber))
