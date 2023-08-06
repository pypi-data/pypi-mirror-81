
from vsg import rule
from vsg import utils


class rule_001(rule.rule):
    '''
    Checks for line length violations.

    '''

    def __init__(self):
        rule.rule.__init__(self, 'length', '001')
        self.phase = 7
        self.solution = None
        self.fixable = False  # The user will have to fix line length violations
        self.disable = False
        self.length = 120
        self.configuration.append('length')

    def _analyze(self, oFile, oLine, iLineNumber):
        if len(oLine.line) > self.length:
            dViolation = utils.create_violation_dict(iLineNumber)
            self.add_violation(dViolation)

    def _get_solution(self, iLineNumber):
        return 'Reduce line to less than ' + str(self.length) + ' characters'
