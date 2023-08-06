
from vsg import rule
from vsg import check
from vsg import fix
from vsg import utils


class rule_007(rule.rule):
    '''Component rule 007 checks for a single space before the "is" keyword.'''

    def __init__(self):
        rule.rule.__init__(self)
        self.name = 'component'
        self.identifier = '007'
        self.solution = 'Remove extra spaces before "is" keyword.'
        self.phase = 2

    def _analyze(self, oFile, oLine, iLineNumber):
        if oLine.isComponentDeclaration and len(oLine.line.split()) > 2:
            check.is_single_space_before(self, 'is', oLine, iLineNumber)

    def _fix_violations(self, oFile):
        for dViolation in self.violations:
            oLine = utils.get_violating_line(oFile, dViolation)
            fix.enforce_one_space_before_word(self, oLine, 'is')
