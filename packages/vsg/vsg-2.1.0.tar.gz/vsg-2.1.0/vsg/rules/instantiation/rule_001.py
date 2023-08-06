
from vsg import rule
from vsg import check
from vsg import fix
from vsg import utils


class rule_001(rule.rule):
    '''
    Instantiation rule 001 checks for proper indent of instantiations.
    '''

    def __init__(self):
        rule.rule.__init__(self)
        self.name = 'instantiation'
        self.identifier = '001'
        self.solution = 'Ensure proper indentation.'
        self.phase = 4

    def _analyze(self, oFile, oLine, iLineNumber):
        if oLine.isInstantiationDeclaration or oLine.isInstantiationPortAssignment or \
           oLine.isInstantiationPortEnd or oLine.isInstantiationPortKeyword or \
           oLine.isInstantiationGenericAssignment or oLine.isInstantiationGenericEnd or \
           oLine.isInstantiationGenericKeyword:
            check.indent(self, oLine, iLineNumber)

    def _fix_violations(self, oFile):
        for dViolation in self.violations:
            fix.indent(self, utils.get_violating_line(oFile, dViolation))
