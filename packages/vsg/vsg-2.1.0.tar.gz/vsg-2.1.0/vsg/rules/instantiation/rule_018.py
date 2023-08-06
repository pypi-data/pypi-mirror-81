
from vsg import rule
from vsg import check
from vsg import fix
from vsg import utils


class rule_018(rule.rule):
    '''
    Instantiation rule 018 checks for a single space between map and (
    '''

    def __init__(self):
        rule.rule.__init__(self)
        self.name = 'instantiation'
        self.identifier = '018'
        self.solution = 'Ensure a single space exists between "map" and (.'
        self.phase = 2

    def _analyze(self, oFile, oLine, iLineNumber):
        if oLine.isInstantiationGenericKeyword or oLine.isInstantiationPortKeyword:
            check.is_single_space_after(self, 'map', oLine, iLineNumber)

    def _fix_violations(self, oFile):
        for dViolation in self.violations:
            fix.enforce_one_space_after_word(self, utils.get_violating_line(oFile, dViolation), 'map')
