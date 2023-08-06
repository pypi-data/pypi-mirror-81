'''
This module contains functions for rules to fix issues.
'''
from vsg import line
from vsg import utils

import re


def indent(self, oLine):
    '''
    Fixes indent violations.

    Parameters:

      self: (rule object)

      oLine: (line object)
    '''
    oLine.update_line(' '*oLine.indentLevel*self.indentSize + oLine.line.lstrip())


def comment_alignment(self, oFile):
    '''
    Aligns comments across multiple lines.

    Parameters:

      self: (rule object)

      oFile: (vhdlFile object)
    '''
    for sKey in self.dFix['violations']:
        iMaximumCommentColumn = self.dFix['violations'][sKey]['maximumCommentColumn']
        for iLineNumber in self.dFix['violations'][sKey]['line']:
            iCommentColumn = self.dFix['violations'][sKey]['line'][iLineNumber]['commentColumn']
            oLine = oFile.lines[iLineNumber]
            oLine.update_line(oLine.line[:iCommentColumn] + ' '*(iMaximumCommentColumn - iCommentColumn) + oLine.line[iCommentColumn:])


def multiline_alignment(self, oFile, iLineNumber):
    '''
    Indents successive lines of multiline statements.

    Parameters:

      self: (rule object)

      oFile: (vhdlFile object)

      iLineNumber: (integer)
    '''
    oLine = oFile.lines[iLineNumber]
    oLine.update_line(' '*self.dFix['violations'][iLineNumber]['column'] + oLine.line.lstrip())


def lower_case(oLine, sKeyword):
    '''
    Changes word to lowercase.

    Parameters:

      self: (rule object)

      oLine: (line object)

      sKeyword: (string)
    '''
    utils.change_word(oLine, sKeyword, sKeyword.lower())


def upper_case(oLine, sKeyword):
    '''
    Changes word to lowercase.

    Parameters:

      self: (rule object)

      oLine: (line object)

      sKeyword: (string)
    '''
    if '(' in sKeyword:
        sWord = utils.remove_parenthesis_from_word(sKeyword)
        utils.change_word(oLine, sWord, sWord.upper())
    else:
        utils.change_word(oLine, sKeyword, sKeyword.upper())


def upper_case_with_parenthesis(self, oLine, sKeyword):
    '''
    Changes word to lowercase.

    Parameters:

      self: (rule object)

      oLine: (line object)

      sKeyword: (string)
    '''


def enforce_one_space_after_word(self, oLine, sWord):
    '''
    Adds a space after a word.

    Parameters:

      self: (rule object)

      oLine: (line object)

      sWord: (string)
    '''
    enforce_spaces_after_word(self, oLine, sWord, 1)


def enforce_spaces_after_word(self, oLine, sWord, iSpaces):
    '''
    Adds a space after a word.

    Parameters:

      self: (rule object)

      oLine: (line object)

      sWord: (string)

      iSpaces: (integer)
    '''
    oLine.update_line(re.sub(r'(' + sWord + ')(\s*)', r'\1' + ' ' * iSpaces, oLine.line, 1, flags=re.IGNORECASE))


def enforce_one_space_before_word(self, oLine, sWord, fWholeWord=False):
    '''
    Adds a space before word.

    Parameters:

      self: (rule object)

      oLine: (line object)

      sWord: (string)
    '''
    if fWholeWord:
        oLine.update_line(re.sub(r'(\S)\s+(' + sWord + ')', r'\1 \2', oLine.line, 1, flags=re.IGNORECASE))
    else:
        oLine.update_line(re.sub(r'(\S)\s*(' + sWord + ')', r'\1 \2', oLine.line, 1, flags=re.IGNORECASE))


def remove_blank_lines_above(self, oFile, iLineNumber, sUnless=None):
    '''
    This function removes blank lines above a linenumber.
    If sUnless is specified, a single blank line will be left if a line with the sUnless attribute is encountered.

    Parameters:

      self: (rule object)

      oFile: (vhdlFile object)

      iLineNumber: (integer)

      sUnless: (string) (optional)
    '''
    while oFile.lines[iLineNumber - 1].isBlank:
        if sUnless:
            if oFile.lines[iLineNumber - 2].__dict__[sUnless]:
                break
        oFile.lines.pop(iLineNumber - 1)
        iLineNumber -= 1


def remove_blank_lines_below(self, oFile, iLineNumber, sUnless=None):
    '''
    This function removes blank lines below a linenumber.
    If sUnless is specified, a single blank line will be left if a line with the sUnless attribute is encountered.

    Parameters:

      self: (rule object)

      oFile: (vhdlFile object)

      iLineNumber: (integer)

      sUnless: (string) (optional)
    '''
    while oFile.lines[iLineNumber + 1].isBlank:
        if sUnless:
            if oFile.lines[iLineNumber + 2].__dict__[sUnless]:
                break
        oFile.lines.pop(iLineNumber + 1)


def insert_blank_line_above(self, oFile, iLineNumber):
    '''
    This function inserts a blank line above the line specified by iLineNumber.

    Parameters:

      self: (rule object)

      oFile: (vhdlFile object)

      iLineNumber: (integer)
    '''
    oFile.lines.insert(iLineNumber, line.blank_line())
    oFile.lines[iLineNumber].insideArchitectureDeclarativeRegion = oFile.lines[iLineNumber + 1].insideArchitectureDeclarativeRegion


def insert_blank_line_below(self, oFile, iLineNumber):
    '''
    This function inserts a blank line below the line specified by iLineNumber.

    Parameters:

      self: (rule object)

      oFile: (vhdlFile object)

      iLineNumber: (integer)
    '''
    oFile.lines.insert(iLineNumber + 1, line.blank_line())
    oFile.lines[iLineNumber + 1].insideArchitectureDeclarativeRegion = oFile.lines[iLineNumber].insideArchitectureDeclarativeRegion


def replace_is_keyword(oFile, iLineNumber):
    '''
    This function removes the is keyword from a line if it starts with is.
    If the line is empty, it is replaced with a blank line.

    Parameters:

      oFile: (vhdlFile object)

      iLineNumber: (integer)
    '''
    iSearchIndex = iLineNumber
    while True:
        iSearchIndex += 1
        oLine = oFile.lines[iSearchIndex]
        if re.match('^\s*is', oLine.line, re.IGNORECASE):
            oLine.line = re.sub(r'^(\s*)is', r'\1  ', oLine.line)
            oLine.lineLower = oLine.line.lower()
            if re.match('^\s*$', oLine.line):
                oLine.line = ''
                oLine.lineLower = ''
                oLine.isBlank = True
        if oFile.lines[iSearchIndex].isGenericKeyword or oFile.lines[iSearchIndex].isPortKeyword:
            break


def identifier_alignment(self, oFile):
    '''
    Aligns identifiers and colons across multiple lines.

    Parameters:

      self: (rule object)

      oFile: (vhdlFile object)
    '''
    for sKey in self.dFix['violations']:
        for iLineNumber in self.dFix['violations'][sKey]['line']:
            oLine = oFile.lines[iLineNumber]
            lLine = oLine.line.split(':', 1)
            sKeyword = lLine[0].split()[0]
            sIdentifier = ' '.join(lLine[0].split()[1:])
            sLine = ' '*oLine.indentLevel*self.indentSize
            sLine += sKeyword
            sLine += ' '*(self.dFix['violations'][sKey]['maximumKeywordLength'] - len(sKeyword) + 1)
            sLine += sIdentifier
            sLine += ' :' + lLine[1]
            oLine.update_line(sLine)


def remove_begin_label(oLine, sLabelName):
    '''
    Removes a label from the beginning of a line.

    Parameters:

      oLine: (line object)

      sLabelName: (string)
    '''
    oLine.update_line(re.sub('^(\s*)(' + sLabelName + '\s*:\s*)', r'\1', oLine.line, 1))


def remove_end_label(oLine, sLabelName):
    '''
    Removes a label from the end of a line.

    Parameters:

      oLine: (line object)

      sLabelName: (string)
    '''
#    oLine.update_line(re.sub('^(\s*end\s+case)(\s*\w+\s*)(;\s*$)', r'\1\3', oLine.line, 1, flags=re.IGNORECASE))
    oLine.update_line(oLine.line.replace(sLabelName, '', 1))
