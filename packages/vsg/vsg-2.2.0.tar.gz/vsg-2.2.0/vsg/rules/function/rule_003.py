
from vsg import rule
from vsg import fix
from vsg import utils

import re


class rule_003(rule.rule):
    '''
    Function rule 003 checks there is a single space between the function name and the (.
    '''

    def __init__(self):
        rule.rule.__init__(self)
        self.name = 'function'
        self.identifier = '003'
        self.solution = 'Ensure a single space exists between the function name and the (.'
        self.phase = 2

    def _analyze(self, oFile, oLine, iLineNumber):
        if oLine.isFunctionKeyword and function_has_parameters(oLine.line):
            if not re.match('^\s*function\s+\w+\s\(', oLine.lineLower) and \
               not re.match('^\s*impure\s+function\s+\w+\s\(', oLine.lineLower) and \
               not re.match('^\s*pure\s+function\s+\w+\s\(', oLine.lineLower):
                dViolation = utils.create_violation_dict(iLineNumber)
                self.add_violation(dViolation)

    def _fix_violations(self, oFile):
        for dViolation in self.violations:
            fix.enforce_one_space_before_word(self, utils.get_violating_line(oFile, dViolation), '\(')


def function_has_parameters(sString):
    if re.match('^\s*function\s+\w+\s*\(', sString, re.IGNORECASE) or \
       re.match('^\s*[impure|pure]\s+function\s+\w+\s*\(', sString, re.IGNORECASE):
        return True
    else:
        return False
