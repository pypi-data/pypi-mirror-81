
from vsg import rule
from vsg import fix
from vsg import utils

class rule_026(rule.rule):
    '''
    Process rule 026 checks for blank lines between the end of the sensitivity list and process declarative lines.
    '''

    def __init__(self):
        rule.rule.__init__(self, 'process', '026')
        self.solution = 'Ensure a single blank line between the end of the sensitivity list and the next non-blank line.'
        self.phase = 3

    def analyze(self, oFile):
        fCheckForBlanks = False
        fSkipProcess = False
        iBlankCount = 0
        iFailingLineNumber = 0
        for iLineNumber, oLine in enumerate(oFile.lines):
            if not self._is_vsg_off(oLine):
                if oLine.insideProcess:
                    if oLine.isProcessBegin and oLine.isSensitivityListEnd:
                        fSkipProcess = True
                    if oLine.isSensitivityListEnd and oFile.lines[iLineNumber + 1].isProcessBegin:
                        fSkipProcess = True
                    if fSkipProcess:
                        if oLine.isEndProcess:
                            fSkipProcess = False
                        continue  # pragma: no cover
                    if fCheckForBlanks:
                        if oLine.isBlank:
                            iBlankCount += 1
                        else:
                            if not iBlankCount == 1 and not oLine.isProcessBegin:
                                dViolation = utils.create_violation_dict(iFailingLineNumber)
                                self.add_violation(dViolation)
                            fSkipProcess = True
                            fCheckForBlanks = False
                            iBlankCount = 0
                    if oLine.isSensitivityListEnd:
                        fCheckForBlanks = True
                        iFailingLineNumber = iLineNumber

    def _fix_violations(self, oFile):
        for dViolation in self.violations[::-1]:
            iLineNumber = utils.get_violation_line_number(dViolation)
            fix.insert_blank_line_below(self, oFile, iLineNumber)
            oFile.lines[iLineNumber + 1].insideProcess = True
