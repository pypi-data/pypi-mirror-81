
from vsg import rule
from vsg import utils

import re


class rule_021(rule.rule):
    '''
    Port rule 021 checks the **port** keyword is on the same line as the (.
    '''

    def __init__(self):
        rule.rule.__init__(self, 'port', '021')
        self.solution = 'Move the ( to the same line as the "port" keyword.'
        self.phase = 2

    def _analyze(self, oFile, oLine, iLineNumber):
        if oLine.isPortKeyword and '(' not in oLine.lineNoComment:
            dViolation = utils.create_violation_dict(iLineNumber)
            self.add_violation(dViolation)

    def _fix_violations(self, oFile):
        for dViolation in self.violations[::-1]:
            iLineNumber = utils.get_violation_line_number(dViolation)
            oLine = oFile.lines[iLineNumber]
            oLine.update_line(re.sub('port', 'port (', oLine.line, 1, re.IGNORECASE))
            utils.search_for_and_remove_keyword(oFile, iLineNumber, '\(')
