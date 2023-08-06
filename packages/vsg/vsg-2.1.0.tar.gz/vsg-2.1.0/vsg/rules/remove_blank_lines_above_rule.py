
from vsg import rule
from vsg import fix
from vsg import check
from vsg import utils


class remove_blank_lines_above_rule(rule.rule):
    '''
    Component rule 016 checks for a blank line above the "end component" keywords.
    '''

    def __init__(self, name=None, identifier=None, sTrigger=None, sUnless=None):
        rule.rule.__init__(self, name, identifier)
        self.solution = None
        self.phase = 3
        self.sTrigger = sTrigger
        self.sUnless = sUnless

    def _analyze(self, oFile, oLine, iLineNumber):
        if oLine.__dict__[self.sTrigger]:
            check.is_no_blank_line_before(self, oFile, iLineNumber, self.sUnless)

    def _fix_violations(self, oFile):
        for dViolation in self.violations[::-1]:
            fix.remove_blank_lines_above(self, oFile, utils.get_violation_line_number(dViolation), self.sUnless)
