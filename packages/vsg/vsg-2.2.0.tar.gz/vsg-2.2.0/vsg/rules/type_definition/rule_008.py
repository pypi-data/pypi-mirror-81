
from vsg import rule
from vsg import line
from vsg import utils

import re


class rule_008(rule.rule):
    '''
    Type rule 008 checks the closing parenthesis of a multi-line type declaration is on it's own line.
    '''

    def __init__(self):
        rule.rule.__init__(self, 'type', '008')
        self.solution = 'Move the closing parenthesis to it\'s own line.'
        self.phase = 1

    def _analyze(self, oFile, oLine, iLineNumber):
        if oLine.isTypeEnumeratedEnd and not oLine.isTypeEnumeratedKeyword:
            if not re.match('^\s*\)\s*;', oLine.lineLower):
                dViolation = utils.create_violation_dict(iLineNumber)
                self.add_violation(dViolation)

    def _fix_violations(self, oFile):
        for dViolation in self.violations[::-1]:
            iLineNumber = utils.get_violation_line_number(dViolation)
            oFile.lines[iLineNumber].line = utils.remove_closing_parenthesis_and_semicolon(oFile.lines[iLineNumber].line)
            oFile.lines[iLineNumber].isTypeEnd = False
            oFile.lines[iLineNumber].isTypeEnumeratedEnd = False
            oFile.lines.insert(iLineNumber + 1, line.line('  );'))
            oFile.lines[iLineNumber + 1].isTypeEnd = True
            oFile.lines[iLineNumber + 1].isTypeEnumeratedEnd = True
            oFile.lines[iLineNumber + 1].insideTypeEnumerated = True
            oFile.lines[iLineNumber + 1].indentLevel = oFile.lines[iLineNumber].indentLevel - 1
            oFile.lines[iLineNumber + 1].insideArchitectureDeclarativeRegion = oFile.lines[iLineNumber].insideArchitectureDeclarativeRegion
            oFile.lines[iLineNumber + 1].insideArchitecture = oFile.lines[iLineNumber].insideArchitecture
