
from vsg import rule
from vsg import check
from vsg import fix
from vsg import utils


class rule_003(rule.rule):
    '''
    Variable assignment rule 003 checks for a single space before the ":=" keyword.
    '''

    def __init__(self):
        rule.rule.__init__(self, 'variable_assignment', '003')
        self.solution = 'Ensure a single space exists before the ":=" keyword.'
        self.phase = 2

    def _analyze(self, oFile, oLine, iLineNumber):
        if oLine.isVariableAssignment:
            check.is_single_space_before_character(self, ':=', oLine, iLineNumber)

    def _fix_violations(self, oFile):
        for dViolation in self.violations:
            fix.enforce_one_space_before_word(self, utils.get_violating_line(oFile, dViolation), ':=')
