
from vsg import rule
from vsg import utils

import re


class rule_023(rule.rule):
    '''If rule 023 checks the "elsif" keyword is on it's own line.'''

    def __init__(self):
        rule.rule.__init__(self)
        self.name = 'if'
        self.identifier = '023'
        self.solution = 'Move "elsif" keyword to it\'s own line.'
        self.phase = 1

    def _analyze(self, oFile, oLine, iLineNumber):
        if oLine.isElseIfKeyword and not re.match('^\s*elsif', oLine.lineLower):
            dViolation = utils.create_violation_dict(iLineNumber)
            self.add_violation(dViolation)

    def _fix_violations(self, oFile):
        for dViolation in self.violations[::-1]:
            iLineNumber = utils.get_violation_line_number(dViolation)
            utils.split_line_before_word(oFile, iLineNumber, 'elsif')
            oFile.lines[iLineNumber].isLastEndIf = False
            oFile.lines[iLineNumber].isElseIfKeyword = False
            oFile.lines[iLineNumber + 1].isIfKeyword = False
            oFile.lines[iLineNumber + 1].isFirstIf = False
