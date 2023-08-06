
from vsg import rule
from vsg import line
from vsg import utils

import re


class rule_010(rule.rule):
    '''Generic rule 010 checks the closing parenthesis for generics are on a line by itself.'''

    def __init__(self):
        rule.rule.__init__(self)
        self.name = 'generic'
        self.identifier = '010'
        self.solution = 'Closing parenthesis must be on a line by itself.'
        self.phase = 1

    def _analyze(self, oFile, oLine, iLineNumber):
        if oLine.isEndGenericMap and not re.match('^\s*\)', oLine.line):
            dViolation = utils.create_violation_dict(iLineNumber)
            self.add_violation(dViolation)

    def _fix_violations(self, oFile):
        for dViolation in self.violations[::-1]:
            iLineNumber = utils.get_violation_line_number(dViolation)
            oFile.lines[iLineNumber].line = utils.remove_closing_parenthesis_and_semicolon(oFile.lines[iLineNumber].line)
            oFile.lines[iLineNumber].isEndGenericMap = False
            oFile.lines.insert(iLineNumber + 1, line.line('  );'))
            oFile.lines[iLineNumber + 1].isEndGenericMap = True
            oFile.lines[iLineNumber + 1].insideGenericMap = True
            if oFile.lines[iLineNumber].isGenericKeyword:
                oFile.lines[iLineNumber + 1].indentLevel = oFile.lines[iLineNumber].indentLevel
            else:
                oFile.lines[iLineNumber + 1].indentLevel = oFile.lines[iLineNumber].indentLevel
                oFile.lines[iLineNumber].indentLevel = oFile.lines[iLineNumber].indentLevel + 1
