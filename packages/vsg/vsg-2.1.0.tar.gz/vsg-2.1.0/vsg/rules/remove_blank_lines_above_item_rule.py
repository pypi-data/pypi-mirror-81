
from vsg import rule_item
from vsg import utils
from vsg import parser


class remove_blank_lines_above_item_rule(rule_item.Rule):
    '''
    Checks for excessive blank lines above a line containing an item.

    Parameters
    ----------

    name : string
       The group the rule belongs to.

    identifier : string
       unique identifier.  Usually in the form of 00N.

    sTrigger : string
       The line attribute the rule applies to.
    '''

    def __init__(self, name, identifier, trigger):
        rule_item.Rule.__init__(self, name=name, identifier=identifier)
        self.phase = 3
        self.trigger = trigger

    def analyze(self, oFile):
        self._print_debug_message('Analyzing rule: ' + self.name + '_' + self.identifier)
        lContexts = self._get_regions(oFile)
        for dContext in lContexts:
            bItemFound = False
            iRemove = -1
            for iLine, oLine in enumerate(dContext['lines'][::-1]):
                lObjects = oLine.get_objects()
                if bItemFound:
                    
                    if oLine.is_blank():
                        iRemove += 1
                    else:
                        if iRemove > 0:
                            dViolation = utils.create_violation_dict(iItemLineNumber)
                            dViolation['iRemove'] = iRemove
                            dViolation['solution'] = 'Remove all but one blank line above this line.'
                            self.add_violation(dViolation)
                        bItemFound = False
                        iRemove = -1
                else:
                    for oObject in lObjects:
                        if isinstance(oObject, self.trigger):
                            iItemLineNumber = dContext['metadata']['iEndLineNumber'] - iLine
                            bItemFound = True

    def _fix_violation(self, oFile, dViolation):
        iStartLineNumber = utils.get_violation_line_number(dViolation) - 1
        for i in range (dViolation['iRemove']):
            oFile.remove_line(iStartLineNumber)
