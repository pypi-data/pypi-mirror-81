
from vsg import rule
from vsg import fix
from vsg import utils

import re


class rule_015(rule.rule):
    '''If rule 015 checks there is a single space between the "end" and "if" keywords.'''

    def __init__(self):
        rule.rule.__init__(self)
        self.name = 'if'
        self.identifier = '015'
        self.solution = 'Ensure only a single space exists between the "end" and "if" keywords.'
        self.phase = 2

    def _analyze(self, oFile, oLine, iLineNumber):
        if oLine.isEndIfKeyword:
            if re.match('^\s*end\s+if', oLine.line, re.IGNORECASE):
                if not re.match('^\s*end\sif', oLine.line, re.IGNORECASE):
                    dViolation = utils.create_violation_dict(iLineNumber)
                    self.add_violation(dViolation)

    def _fix_violations(self, oFile):
        for dViolation in self.violations:
            fix.enforce_one_space_after_word(self, utils.get_violating_line(oFile, dViolation), 'end')
