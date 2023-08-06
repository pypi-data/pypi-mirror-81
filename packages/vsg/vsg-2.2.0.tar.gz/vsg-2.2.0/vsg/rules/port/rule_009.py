
from vsg import rule
from vsg import fix
from vsg import check
from vsg import utils

import re


class rule_009(rule.rule):
    '''
    Port rule 009 checks for a single space after "inout" keyword in a port declaration for "inout" ports.
    '''

    def __init__(self):
        rule.rule.__init__(self)
        self.name = 'port'
        self.identifier = '009'
        self.solution = 'Change the number of spaces after the "inout" keyword to one space.'
        self.phase = 2

    def _analyze(self, oFile, oLine, iLineNumber):
        if oLine.isPortDeclaration and re.match('^\s*\S+\s*:\s*inout', oLine.lineLower):
            check.is_single_space_after(self, 'inout', oLine, iLineNumber)

    def _fix_violations(self, oFile):
        for dViolation in self.violations:
            oLine = utils.get_violating_line(oFile, dViolation)
            fix.enforce_one_space_after_word(self, oLine, 'inout')
