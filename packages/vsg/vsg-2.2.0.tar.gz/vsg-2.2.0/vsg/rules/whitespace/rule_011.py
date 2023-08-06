
from vsg import rule
from vsg import utils

import re


class rule_011(rule.rule):
    '''Whitespace rule 011 checks for spaces before and after math operators.'''

    def __init__(self):
        rule.rule.__init__(self)
        self.name = 'whitespace'
        self.identifier = '011'
        self.phase = 2
        self.solution = 'Add a single space before and/or after math operator.'

    def _analyze(self, oFile, oLine, iLineNumber):
        sLine = utils.remove_comment(oLine.line)
        if sLine[-2:] == '--':
            sLine = sLine[:-2]
        if '-' in sLine:
            lLine = sLine.split()
            for sWord in lLine:
                if '-' in sWord:
                    if sWord == '-':
                        # already good.
                        continue
                    if re.match(r".*?'-'", sWord) is not None:
                        # found a std_logic don't care.
                        continue
                    if re.match(r'(?:".*"|[^"\n])*?-', sWord) is None:
                        # The - was in a quoted string.
                        # e.g. found a std_logic_vector constant with a don't care.
                        continue
                    #if re.match('^.*\W-[0-9]', sWord) is not None:
                    #    # found a negative number
                    #    continue
                    if re.match('^.*\w-', sWord):
                        dViolation = utils.create_violation_dict(iLineNumber)
                        self.add_violation(dViolation)
                    elif not re.match('^.*-[0-9]+\)?$', sWord):
                        dViolation = utils.create_violation_dict(iLineNumber)
                        self.add_violation(dViolation)
        else:
            if re.match('^.*[\w+|\)][+|/|*]', sLine) or re.match('^.*[+|/|*][\w+|\(]', sLine):
                if not re.match('^.*".*/.*"', sLine):
                    dViolation = utils.create_violation_dict(iLineNumber)
                    self.add_violation(dViolation)

    def _fix_violations(self, oFile):
        for dViolation in self.violations:
            oLine = utils.get_violating_line(oFile, dViolation)
            iCommentIndex = oLine.line.find('--')
            if iCommentIndex == -1:
                oLine.update_line(re.sub(r'(\w+)([+|\-|/|*])', r'\1 \2', oLine.line))
                oLine.update_line(re.sub(r'\)([+|\-|/|*])', r') \1', oLine.line))
                oLine.update_line(re.sub(r'([+|\-|/|*])(\w+)', r'\1 \2', oLine.line))
                oLine.update_line(re.sub(r'([+|\-|/|*])\(', r'\1 (', oLine.line))
            else:
                sLine = oLine.line[:iCommentIndex]
                sLine = re.sub(r'(\w+)([+|\-|/|*])', r'\1 \2', sLine)
                sLine = re.sub(r'\)([+|\-|/|*])', r') \1', sLine)
                sLine = re.sub(r'([+|\-|/|*])(\w+)', r'\1 \2', sLine)
                sLine = re.sub(r'([+|\-|/|*])\(', r'\1 (', sLine)
                sLine = sLine + oLine.line[iCommentIndex:]
                oLine.update_line(sLine)
