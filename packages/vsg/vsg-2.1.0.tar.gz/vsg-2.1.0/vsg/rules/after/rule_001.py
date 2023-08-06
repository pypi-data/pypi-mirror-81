
import re

from vsg import rule
from vsg import utils


class rule_001(rule.rule):
    '''
    After rule 001 checks for the "after" keyword in signal assignments in clock processes.
    '''

    def __init__(self):
        rule.rule.__init__(self, 'after', '001')
        self.phase = 1
        self.disable = True
        self.magnitude = 1
        self.units = 'ns'
        self.configuration.extend(['magnitude', 'units'])
        self.solution = 'Add after ' + str(self.magnitude) + ' ' + self.units + ' to signal in clock process'

    def _pre_analyze(self):
        self.sequentialStatement = ""

    def _analyze(self, oFile, oLine, iLineNumber):
        if oLine.insideClockProcess:
            if oLine.isSequentialEnd:
                self.sequentialStatement += oLine.lineNoComment + " "
                if not re.match('^\s*.*\safter\s', self.sequentialStatement):
                    dViolation = utils.create_violation_dict(iLineNumber)
                    self.add_violation(dViolation)
                self.sequentialStatement = ""
            elif oLine.insideSequential:
                self.sequentialStatement += oLine.lineNoComment + " "
            elif oLine.isSequential:
                self.sequentialStatement = oLine.lineNoComment + " "

    def _fix_violations(self, oFile):
        for dViolation in self.violations:
            oLine = utils.get_violating_line(oFile, dViolation)
            sLine = oLine.line
            sNewLine = sLine.replace(';', ' ' + ' '.join(['after', str(self.magnitude), self.units]) + ';')
            oLine.update_line(sNewLine)
