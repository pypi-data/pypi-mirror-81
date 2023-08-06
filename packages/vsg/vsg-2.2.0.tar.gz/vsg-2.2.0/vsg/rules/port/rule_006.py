
from vsg import rule
from vsg import fix
from vsg import check
from vsg import utils

import re


class rule_006(rule.rule):
    '''
    Port rule 006 checks for one space after the colon in a port declaration for "out" ports.
    '''

    def __init__(self):
        rule.rule.__init__(self, 'port', '006')
        self.solution = 'Change number of spaces after : to a single space.'
        self.phase = 2

    def _analyze(self, oFile, oLine, iLineNumber):
        if oLine.isPortDeclaration and re.match('^.*:\s*out', oLine.line, re.IGNORECASE):
            check.is_single_space_after_character(self, ':', oLine, iLineNumber)

    def _fix_violations(self, oFile):
        for dViolation in self.violations:
            oLine = utils.get_violating_line(oFile, dViolation)
            fix.enforce_one_space_after_word(self, oLine, ':')
