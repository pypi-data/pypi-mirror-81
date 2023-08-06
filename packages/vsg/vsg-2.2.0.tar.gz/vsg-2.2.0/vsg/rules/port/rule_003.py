
from vsg import rule
from vsg import check
from vsg import fix
from vsg import utils


class rule_003(rule.rule):
    '''
    Port rule 003 checks spacing between "port" and the open parenthesis.
    '''

    def __init__(self):
        rule.rule.__init__(self)
        self.name = 'port'
        self.identifier = '003'
        self.solution = 'Change spacing between "port" and "(" to one space.'
        self.phase = 2

    def _analyze(self, oFile, oLine, iLineNumber):
        if oLine.isPortKeyword and '(' in oLine.line:
            check.is_single_space_after(self, 'port', oLine, iLineNumber)

    def _fix_violations(self, oFile):
        for dViolation in self.violations:
            oLine = utils.get_violating_line(oFile, dViolation)
            fix.enforce_one_space_after_word(self, oLine, 'port')
