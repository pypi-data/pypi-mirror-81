
from vsg import rule
from vsg import utils

import re


class rule_022(rule.rule):
    '''If rule 022 checks for code after the "else" keyword.'''

    def __init__(self):
        rule.rule.__init__(self)
        self.name = 'if'
        self.identifier = '022'
        self.solution = 'Move code after "else" keyword to the next line.'
        self.phase = 1

    def _analyze(self, oFile, oLine, iLineNumber):
        if oLine.isElseKeyword and re.match('^.*else\s+\w', oLine.lineLower):
            dViolation = utils.create_violation_dict(iLineNumber)
            self.add_violation(dViolation)

    def _fix_violations(self, oFile):
        for dViolation in self.violations[::-1]:
            iLineNumber = utils.get_violation_line_number(dViolation)
            utils.split_line_after_word(oFile, iLineNumber, 'else')
            oFile.lines[iLineNumber + 1].isElseKeyword = False
            oFile.lines[iLineNumber].isIfKeyword = False
            oFile.lines[iLineNumber].isElseIfKeyword = False
            oFile.lines[iLineNumber].isThenKeyword = False
            oFile.lines[iLineNumber + 1].indentLevel += 1
            oFile.lines[iLineNumber].isLastEndIf = False
            utils.reclassify_line(oFile, iLineNumber)
            oFile.lines[iLineNumber + 1].isFirstIf = False
