
from vsg import rule
from vsg import utils

import re


class rule_005(rule.rule):
    '''
    Package rule 005 checks if the "is" keyword is on the same line as the "package" keyword.
    '''

    def __init__(self):
        rule.rule.__init__(self)
        self.name = 'package'
        self.identifier = '005'
        self.solution = 'Ensure "is" keyword is on the same line as the "package" keyword.'
        self.phase = 1

    def _analyze(self, oFile, oLine, iLineNumber):
        if oLine.isPackageKeyword:
            lLine = oLine.lineLower.split()
            if len(lLine) < 3 or not lLine[2] == "is":
                dViolation = utils.create_violation_dict(iLineNumber)
                self.add_violation(dViolation)

    def _fix_violations(self, oFile):
        for dViolation in self.violations:
            iLineNumber = utils.get_violation_line_number(dViolation)
            oLine = oFile.lines[iLineNumber]
            oLine.update_line(re.sub(r'^(\s*package\s+\w+)', r'\1 is', oLine.line, re.IGNORECASE))
            # Search for "is" on the next line
            iSearchIndex = iLineNumber
            while True:
                iSearchIndex += 1
                oLine = oFile.lines[iSearchIndex]
                if re.match('^\s*is', oLine.line, re.IGNORECASE):
                    oLine.update_line(re.sub(r'^(\s*)is', r'\1  ', oLine.line))
                    if re.match('^\s*$', oLine.line):
                        oLine.update_line('')
                        oLine.isBlank = True
                        break
                if not oLine.isBlank:
                    break
