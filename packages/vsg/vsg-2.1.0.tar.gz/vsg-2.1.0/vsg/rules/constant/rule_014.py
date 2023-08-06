
import re

from vsg import rule
from vsg import utils


class rule_014(rule.rule):
    '''
    Constant rule 014 checks the indent of multiline constants that are not arrays.
    '''

    def __init__(self):
        rule.rule.__init__(self)
        self.name = 'constant'
        self.identifier = '014'
        self.solution = 'Align with := keyword on constant declaration line.'
        self.phase = 5

    def _pre_analyze(self):
        self.alignmentColumn = 0
        self.fKeywordFound = False

    def _analyze(self, oFile, oLine, iLineNumber):
        if not oLine.isConstantArray and oLine.insideConstant:
            if oLine.isConstant and ':=' in oLine.line:
                self.alignmentColumn = oLine.line.index(':=') + len(':= ')
                self.fKeywordFound = True
            elif not oLine.isConstant and self.fKeywordFound:
                sMatch = ' ' * self.alignmentColumn
                if not re.match('^' + sMatch + '\w', oLine.line):
                    dViolation = utils.create_violation_dict(iLineNumber)
                    dViolation['column'] = self.alignmentColumn
                    self.add_violation(dViolation)
            if oLine.isConstantEnd:
                self.fKeywordFound = False

    def _fix_violations(self, oFile):
        for dViolation in self.violations:
            iLineNumber = utils.get_violation_line_number(dViolation)
            sLine = oFile.lines[iLineNumber].line
            sNewLine = ' ' * dViolation['column'] + sLine.strip()
            oFile.lines[iLineNumber].update_line(sNewLine)
