
from vsg import rule
from vsg import fix
from vsg import check
from vsg import utils


class remove_blank_lines_below_rule(rule.rule):
    '''
    Checks for and removes blank lines based on a trigger.
    '''

    def __init__(self, name=None, identifier=None, sTrigger=None, sUnless=None):
        rule.rule.__init__(self, name, identifier)
        self.solution = None
        self.phase = 3
        self.sTrigger = sTrigger
        self.sUnless = sUnless

    def _analyze(self, oFile, oLine, iLineNumber):
        if oLine.__dict__[self.sTrigger]:
            check.is_no_blank_line_after(self, oFile, iLineNumber, self.sUnless)

    def _fix_violations(self, oFile):
        for dViolation in self.violations[::-1]:
            iLineNumber = utils.get_violation_line_number(dViolation)
            fix.remove_blank_lines_below(self, oFile, iLineNumber, self.sUnless)
