
from vsg import rule
from vsg import check
from vsg import fix
from vsg import utils


class single_space_before_rule(rule.rule):
    '''
    Single space before rule checks for a single space before a user specified keyword.
    '''

    def __init__(self, name=None, identifier=None, sTrigger=None, sWord=None, fWholeWord=False):
        rule.rule.__init__(self, name=name, identifier=identifier)
        self.phase = 2
        self.sTrigger = sTrigger
        self.sWord = sWord
        self.solution = None
        self.fWholeWord = fWholeWord

    def _analyze(self, oFile, oLine, iLineNumber):
        if oLine.__dict__[self.sTrigger]:
            check.is_single_space_before(self, self.sWord, oLine, iLineNumber)

    def _fix_violations(self, oFile):
        for dViolation in self.violations:
            oLine = utils.get_violating_line(oFile, dViolation)
            fix.enforce_one_space_before_word(self, oLine, self.sWord, self.fWholeWord)
