
from vsg import rule
from vsg import check
from vsg import fix
from vsg import utils

import re


class rule_022(rule.rule):
    '''
    Architecture rule 022 checks for a single space after the "end architecture" keywords and the architecture name.
    '''

    def __init__(self):
        rule.rule.__init__(self, 'architecture', '022')
        self.solution = 'Ensure a single space exists between "architecture" and the architecture name.'
        self.phase = 2

    def _analyze(self, oFile, oLine, iLineNumber):
        if oLine.isEndArchitecture and re.match('^\s*end\s+architecture\s+\w', oLine.lineLower):
            check.is_single_space_after(self, 'architecture', oLine, iLineNumber)

    def _fix_violations(self, oFile):
        for dViolation in self.violations:
            fix.enforce_one_space_after_word(self, utils.get_violating_line(oFile, dViolation), 'architecture')
