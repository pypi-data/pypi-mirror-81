
from vsg import rule
from vsg import fix
from vsg import check
from vsg import utils

import re


class rule_005(rule.rule):
    '''
    Port rule 005 checks for a single space after the colon in a port declaration for "in" and "inout" ports.
    '''

    def __init__(self):
        rule.rule.__init__(self)
        self.name = 'port'
        self.identifier = '005'
        self.solution = 'Reduce number of spaces after the colon to 1.'
        self.phase = 2

    def _analyze(self, oFile, oLine, iLineNumber):
        if oLine.isPortDeclaration and re.match('^.*:\s*in', oLine.line, re.IGNORECASE):
            check.is_single_space_after_character(self, ':', oLine, iLineNumber)

    def _fix_violations(self, oFile):
        for dViolation in self.violations:
            oLine = utils.get_violating_line(oFile, dViolation)
            fix.enforce_one_space_after_word(self, oLine, ':')
