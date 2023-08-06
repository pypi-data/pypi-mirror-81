
from vsg.rules import single_space_before_character_rule


class rule_006(single_space_before_character_rule):
    '''
    Variable rule 006 checks there is at least a single space before the colon.
    '''

    def __init__(self):
        single_space_before_character_rule.__init__(self, 'variable', '006', 'isVariable', ':')
        self.solution = 'Add a single space before the colon.'
