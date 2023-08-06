
from vsg import rule
from vsg import utils

import re


class rule_009(rule.rule):
    '''
    Type rule 009 checks for enumerated types after the open parenthesis on a multi-line type declaration.
    '''

    def __init__(self):
        rule.rule.__init__(self, 'type', '009')
        self.solution = 'Move enumerated type to it\'s own line.'
        self.phase = 1

    def _analyze(self, oFile, oLine, iLineNumber):
        if oLine.isTypeEnumeratedKeyword and not oLine.isTypeEnumeratedEnd:
            if re.match('^.*\sis\s*\(\s*\w', oLine.lineLower):
                dViolation = utils.create_violation_dict(iLineNumber)
                self.add_violation(dViolation)

    def _fix_violations(self, oFile):
        for dViolation in self.violations[::-1]:
            iLineNumber = utils.get_violation_line_number(dViolation)
            utils.split_line_after_word(oFile, iLineNumber, '(')
            oLine = oFile.lines[iLineNumber + 1]
            oLine.isTypeKeyword = False
            oLine.isTypeEnumeratedKeyword = False
            oLine.indentLevel += 1
