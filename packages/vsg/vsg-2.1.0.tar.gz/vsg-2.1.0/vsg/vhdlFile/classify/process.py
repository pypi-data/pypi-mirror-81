import re


def process(dVars, oLine, lLines):
    '''
    Classifies process statements.

    [process_label :] process [(signal_name {,...})] [is]
        { process_declarative_item }
    begin
      { sequential_statement }
    end process [process_label] ;

    Sets the following line attributes:

      * insideProcess
      * isProcessKeyword
      * indentLevel
      * isProcessLabel
      * isSensitivityListBegin
      * insideSensitivityList
      * isSensitivityListEnd
      * isProcessBegin
      * isEndProcess
      * insideClockProcess
      * insideResetProcess
      * isProcessIs

    Modifies the following variables:

      * iProcessIndentLevel
      * fFoundProcessBegin
      * SensitivityListFound
      * iOpenParenthesis
      * iCloseParenthesis
      * iCurrentIndentLevel

    '''
    classify_process_keyword(dVars, oLine)
    if oLine.insideProcess:
        classify_process_sensitivity_list(dVars, oLine)
        classify_is_keyword(dVars, oLine)
        classify_process_begin_keyword(dVars, oLine)
        classify_process_end_keyword(dVars, oLine)
        classify_clock_process(dVars, oLine, lLines)


def classify_process_keyword(dVars, oLine):
    if re.match('^\s*process[:|\s|(]', oLine.lineLower):
        oLine.isProcessKeyword = True
        oLine.insideProcess = True
        dVars['iProcessIndentLevel'] = dVars['iCurrentIndentLevel']
        oLine.indentLevel = dVars['iCurrentIndentLevel']
        if re.match('^\s*process\s+is', oLine.lineLower):
            dVars['iCurrentIndentLevel'] += 1
    if re.match('^\s*process\s*$', oLine.lineNoComment):
        oLine.isProcessKeyword = True
        oLine.insideProcess = True
        dVars['iProcessIndentLevel'] = dVars['iCurrentIndentLevel']
        oLine.indentLevel = dVars['iCurrentIndentLevel']
        dVars['iCurrentIndentLevel'] += 1
    if re.match('^\s*\S+\s*:\s*process', oLine.lineLower) and not oLine.isComment:
        oLine.isProcessKeyword = True
        oLine.insideProcess = True
        dVars['iProcessIndentLevel'] = dVars['iCurrentIndentLevel']
        oLine.indentLevel = dVars['iCurrentIndentLevel']
        oLine.isProcessLabel = True
        if re.match('^\s*\S+\s*:\s*process\s+is', oLine.lineLower):
            dVars['iCurrentIndentLevel'] += 1
    if re.match('^\s*\S+\s*:\s*process\s*$', oLine.lineNoComment) and not oLine.isComment:
        dVars['iProcessIndentLevel'] = dVars['iCurrentIndentLevel']
        dVars['iCurrentIndentLevel'] += 1


def classify_process_sensitivity_list(dVars, oLine):
    # Check sensitivity list
    if '(' in oLine.line and \
       not oLine.insideProcedure and \
       not oLine.insideSensitivityList and \
       not dVars['fFoundProcessBegin'] and \
       not dVars['SensitivityListFound'] and \
       not oLine.isVariable:
        oLine.isSensitivityListBegin = True
        oLine.insideSensitivityList = True
        dVars['SensitivityListFound'] = True
    if oLine.insideSensitivityList:
        dVars['iOpenParenthesis'] += oLine.line.count('(')
        dVars['iCloseParenthesis'] += oLine.line.count(')')
        if dVars['iOpenParenthesis'] == dVars['iCloseParenthesis']:
            oLine.isSensitivityListEnd = True
            dVars['iOpenParenthesis'] = 0
            dVars['iCloseParenthesis'] = 0
            dVars['iCurrentIndentLevel'] += 1


def classify_process_begin_keyword(dVars, oLine):
    if not oLine.insideProcedure and not oLine.insideFunction:
        if re.match('^.*\s+begin', oLine.lineNoComment, flags=re.IGNORECASE) or re.match('^\s*begin', oLine.lineLower):
            oLine.indentLevel = dVars['iProcessIndentLevel']
            oLine.isProcessBegin = True
            dVars['fFoundProcessBegin'] = True


def classify_process_end_keyword(dVars, oLine):
    if re.match('^\s*end\s+process', oLine.lineLower):
        oLine.indentLevel = dVars['iProcessIndentLevel']
        oLine.isEndProcess = True
        dVars['fFoundProcessBegin'] = False
        dVars['iCurrentIndentLevel'] = dVars['iCurrentIndentLevel'] - 1
        dVars['SensitivityListFound'] = False
    if re.match('^\s*end\s+process\s+\S+\s*;', oLine.lineLower):
        oLine.isProcessEndLabel = True


def classify_clock_process(dVars, oLine, lLines):
    if re.match('^\s*[elsif|if]\s*.*\'event\s+and\s+[a-zA-Z0-9_.]+\s*=\s*\'[0-1]\'', oLine.lineNoComment, flags=re.IGNORECASE):
        oLine.insideClockProcess = True
        oLine.isClockStatement = True
        classify_reset_process(oLine, lLines)
    if re.match('^\s*[elsif|if]\s*.*rising_edge', oLine.lineNoComment, flags=re.IGNORECASE):
        oLine.insideClockProcess = True
        oLine.isClockStatement = True
        classify_reset_process(oLine, lLines)
    if re.match('^\s*[elsif|if]\s*.*falling_edge', oLine.lineNoComment, flags=re.IGNORECASE):
        oLine.insideClockProcess = True
        oLine.isClockStatement = True
        classify_reset_process(oLine, lLines)


def classify_reset_process(oLine, lLines):
    if re.match('^\s*if', oLine.lineNoComment, flags=re.IGNORECASE):
        return

    iIndex = len(lLines) - 1

    while lLines[iIndex].isIfKeyword is False:
        lLines[iIndex].insideResetProcess = True
        iIndex = iIndex - 1
    lLines[iIndex].insideResetProcess = True


def classify_is_keyword(dVars, oLine):
    if not dVars['fFoundProcessBegin']:
        if re.match('^.*[\s|\)]is[\s|\-\-]', oLine.lineNoComment, flags=re.IGNORECASE) or \
           re.match('^.*[\s|\)]is$', oLine.lineNoComment, flags=re.IGNORECASE):
            oLine.isProcessIs = True
