
from vsg.rules import case_rule
from vsg import utils


class rule_003(case_rule):
    '''
    For Loop rule 003 checks the label has proper case.
    '''

    def __init__(self):
        case_rule.__init__(self, 'for_loop', '003', 'isForLoopLabel')
        self.solution = 'Change label to ' + self.case + 'case'

    def _extract(self, oLine):
        return [oLine.lineNoComment.replace(':', ' ').split()[0]]
