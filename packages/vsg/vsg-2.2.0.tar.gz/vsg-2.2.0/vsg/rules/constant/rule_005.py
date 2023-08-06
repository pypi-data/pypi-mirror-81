
from vsg import rule
from vsg import fix
from vsg import utils

import re


class rule_005(rule.rule):
    '''
    Constant rule 005 checks there is a single space after the colon.
    '''

    def __init__(self):
        rule.rule.__init__(self)
        self.name = 'constant'
        self.identifier = '005'
        self.solution = 'Ensure only a single space after the colon.'
        self.phase = 2

    def _analyze(self, oFile, oLine, iLineNumber):
        if oLine.isConstant:
            if not re.match('^\s*constant\s+\w+\s*:\s\w', oLine.lineLower):
                dViolation = utils.create_violation_dict(iLineNumber)
                self.add_violation(dViolation)

    def _fix_violations(self, oFile):
        for dViolation in self.violations:
            fix.enforce_one_space_after_word(self, utils.get_violating_line(oFile, dViolation), ':')
