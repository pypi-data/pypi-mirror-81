
from vsg import rule
from vsg import utils

import re


class rule_016(rule.rule):
    '''
    Generic rule 016 checks for multiple generic terms on a single line.
    '''

    def __init__(self):
        rule.rule.__init__(self)
        self.name = 'generic'
        self.identifier = '016'
        self.solution = 'Move multiple generics to their own lines.'
        self.phase = 1

    def _analyze(self, oFile, oLine, iLineNumber):
        if oLine.isGenericDeclaration and re.match('^.*;.*:', oLine.lineNoComment):
            dViolation = utils.create_violation_dict(iLineNumber)
            self.add_violation(dViolation)

    def _fix_violations(self, oFile):
        for dViolation in self.violations[::-1]:
            iLineNumber = utils.get_violation_line_number(dViolation)
            for i in range(0, oFile.lines[iLineNumber].line.count(';')):
                utils.split_line_after_word(oFile, iLineNumber + i, ';')
