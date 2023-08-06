
from vsg import parser
from vsg.rules import move_item_next_to_another_item_rule


class rule_009(move_item_next_to_another_item_rule):
    '''
    Checks the context keyword is on the same line as the end context keyword.

    '''

    def __init__(self):
        move_item_next_to_another_item_rule.__init__(self, 'context', '009', parser.context_end_keyword, parser.context_end_context_keyword)
        self.solution = None
        self.subphase = 1
        self.regionBegin = parser.context_keyword
        self.regionEnd = parser.context_semicolon
