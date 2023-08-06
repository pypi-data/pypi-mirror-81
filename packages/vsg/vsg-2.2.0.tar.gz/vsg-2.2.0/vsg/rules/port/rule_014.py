
from vsg import rule
from vsg import line
from vsg import utils

import re


class rule_014(rule.rule):
    '''
    Port rule 014 checks the closing parenthesis for ports are on a line by
    itself.
    '''

    def __init__(self):
        rule.rule.__init__(self, 'port', '014')
        self.solution = 'Closing parenthesis must be on a line by itself and \
                         above the "end" keyword.'
        self.phase = 1

    def _analyze(self, oFile, oLine, iLineNumber):
        if oLine.isEndPortMap and not re.match('^\s*\)', oLine.line):
            dViolation = utils.create_violation_dict(iLineNumber)
            self.add_violation(dViolation)

    def _fix_violations(self, oFile):
        for dViolation in self.violations[::-1]:
            iLineNumber = utils.get_violation_line_number(dViolation)
            oFile.lines[iLineNumber].update_line(re.sub(r'\)(\s*);', r' \1 ', oFile.lines[iLineNumber].line))
            oFile.lines[iLineNumber].isEndPortMap = False
            oFile.lines[iLineNumber].indentLevel += 1
            oFile.lines.insert(iLineNumber + 1, line.line('  );'))
            oFile.lines[iLineNumber + 1].isEndPortMap = True
            oFile.lines[iLineNumber + 1].insidePortMap = True
            oFile.lines[iLineNumber + 1].insideEntity = oFile.lines[iLineNumber].insideEntity
            oFile.lines[iLineNumber + 1].indentLevel = oFile.lines[iLineNumber].indentLevel - 1
