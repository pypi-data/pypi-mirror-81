
from vsg import rule
from vsg import fix
from vsg import utils

import re


class rule_009(rule.rule):
    '''
    Package rule 009 checks for a single space between the "end" and "package" keywords and component name.
    '''

    def __init__(self):
        rule.rule.__init__(self, 'package', '009')
        self.solution = 'Single space between "end" and "package" keywords and component name.'
        self.phase = 2

    def _analyze(self, oFile, oLine, iLineNumber):
        if oLine.isPackageEnd:
            check_spaces_between_end_and_package_and_name(self, oLine, iLineNumber)
            check_spaces_between_end_and_package(self, oLine, iLineNumber)
            check_spaces_between_end_and_name(self, oLine, iLineNumber)

    def _fix_violations(self, oFile):
        for dViolation in self.violations:
            iLineNumber = utils.get_violation_line_number(dViolation)
            fix.enforce_one_space_after_word(self, oFile.lines[iLineNumber], 'end')
            fix.enforce_one_space_after_word(self, oFile.lines[iLineNumber], 'package')


def check_spaces_between_end_and_package_and_name(self, oLine, iLineNumber):
    if re.match('^\s*end\s+package\s+\w', oLine.lineLower):
        if not re.match('^\s*end\spackage\s\w', oLine.lineLower):
            dViolation = utils.create_violation_dict(iLineNumber)
            self.add_violation(dViolation)


def check_spaces_between_end_and_package(self, oLine, iLineNumber):
    if re.match('^\s*end\s+package', oLine.lineLower):
        if not re.match('^\s*end\spackage', oLine.lineLower):
            dViolation = utils.create_violation_dict(iLineNumber)
            self.add_violation(dViolation)


def check_spaces_between_end_and_name(self, oLine, iLineNumber):
    if re.match('^\s*end\s+\w', oLine.lineLower):
        if not re.match('^\s*end\s\w', oLine.lineLower):
            dViolation = utils.create_violation_dict(iLineNumber)
            self.add_violation(dViolation)
