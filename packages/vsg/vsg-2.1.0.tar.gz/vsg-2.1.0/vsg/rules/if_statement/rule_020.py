
from vsg import rule
from vsg import utils

import re


class rule_020(rule.rule):
    '''If rule 020 checks the "end if" keyword is on it's own line.'''

    def __init__(self):
        rule.rule.__init__(self)
        self.name = 'if'
        self.identifier = '020'
        self.solution = 'Move "end if" keyword to it\'s own line.'
        self.phase = 1

    def _analyze(self, oFile, oLine, iLineNumber):
        if oLine.isEndIfKeyword and not re.match('^\s*end\s+if', oLine.lineLower):
            dViolation = utils.create_violation_dict(iLineNumber)
            self.add_violation(dViolation)

    def _fix_violations(self, oFile):
        for dViolation in self.violations[::-1]:
            iLineNumber = utils.get_violation_line_number(dViolation)
            utils.split_line_before_word(oFile, iLineNumber, 'end')
            oFile.lines[iLineNumber].isEndIfKeyword = False
            oFile.lines[iLineNumber].isLastEndIf = False
            oFile.lines[iLineNumber + 1].isIfKeyword = False
            oFile.lines[iLineNumber + 1].isElseIfKeyword = False
            oFile.lines[iLineNumber + 1].isElseKeyword = False
            oFile.lines[iLineNumber + 1].isThenKeyword = False
            oFile.lines[iLineNumber + 1].isFirstIf = False
