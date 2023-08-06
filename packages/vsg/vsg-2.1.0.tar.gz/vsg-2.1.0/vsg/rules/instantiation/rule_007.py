
from vsg import rule
from vsg import line
from vsg import utils


class rule_007(rule.rule):
    '''
    Instantiation rule 007 checks the closing ) for the port map is on it's own line.
    '''

    def __init__(self):
        rule.rule.__init__(self)
        self.name = 'instantiation'
        self.identifier = '007'
        self.solution = 'Place closing ); on it\'s own line.'
        self.phase = 1

    def _analyze(self, oFile, oLine, iLineNumber):
        if oLine.isInstantiationPortEnd and oLine.isInstantiationPortAssignment:
            dViolation = utils.create_violation_dict(iLineNumber)
            self.add_violation(dViolation)

    def _fix_violations(self, oFile):
        for dViolation in self.violations[::-1]:
            iLineNumber = utils.get_violation_line_number(dViolation)
            oFile.lines[iLineNumber].line = utils.remove_closing_parenthesis_and_semicolon(oFile.lines[iLineNumber].line)
            oFile.lines[iLineNumber].isInstantiationPortEnd = False
            oFile.lines.insert(iLineNumber + 1, line.line('  );'))
            oFile.lines[iLineNumber + 1].isInstantiationPortAssignement = False
            oFile.lines[iLineNumber + 1].isInstantiationPortEnd = True
            oFile.lines[iLineNumber + 1].insideInstantiation = True
            if oFile.lines[iLineNumber].isInstantiationPortKeyword:
                oFile.lines[iLineNumber + 1].indentLevel = oFile.lines[iLineNumber].indentLevel
            else:
                oFile.lines[iLineNumber + 1].indentLevel = oFile.lines[iLineNumber].indentLevel - 1
