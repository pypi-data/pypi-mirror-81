
from vsg import fix
from vsg import check
from vsg import rule
from vsg import utils


class line_above_rule(rule.rule):
    '''
    Checks for blank lines above a line and will insert a blank line if one does not exist.

    Parameters
    ----------

    name : string
       The group the rule belongs to.

    identifier : string
       unique identifier.  Usually in the form of 00N.

    sTrigger : string
       The line attribute the rule applies to.
    '''

    def __init__(self, name=None, identifier=None, sTrigger=None, sUnless=None):
        rule.rule.__init__(self, name, identifier)
        self.solution = 'Insert blank line above.'
        self.phase = 3
        # The user updates the attributes below
        self.condition = sTrigger
        self.sUnless = sUnless

    def _analyze(self, oFile, oLine, iLineNumber):
        if oLine.__dict__[self.condition]:
            check.is_blank_line_before(self, oFile, iLineNumber, self.sUnless)

    def _fix_violations(self, oFile):
        for dViolation in self.violations[::-1]:
            fix.insert_blank_line_above(self, oFile, utils.get_violation_line_number(dViolation))
