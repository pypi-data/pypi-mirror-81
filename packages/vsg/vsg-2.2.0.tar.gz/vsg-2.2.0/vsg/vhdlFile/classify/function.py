import re


def function(dVars, oLine):
    '''
    Classifies function statements.

    [pure|impure] function identifier [ (parameter_interface_list) ] return type_mark is
      [ subprogram_declarative_part ]
    begin
      { sequential_statement }
    end [function] [identifier] ;

    Sets the following line attributes:

      * insideFunction
      * insideFunctionDeclarative
      * isFunctionParameter
      * isFunctionParameterEnd
      * isFunctionBegin
      * isFunctionKeyword
      * isFunctionEnd
      * isFunctionReturn
      * isFunctionIs

    Modifies the following variables:

      * iOpenParenthesis
      * iCurrentIndentLevel
      * fFunctionParameterEndDetected
      * fFunctionIsDetected
      * fFunctionBeginDetected
    '''
    _classify_function_keyword(dVars, oLine)
    if oLine.insideFunction:
        dVars['iOpenParenthesis'] += oLine.lineNoComment.count('(')
        dVars['iCloseParenthesis'] += oLine.lineNoComment.count(')')
        _classify_return_type(dVars, oLine)
        _classify_is(dVars, oLine)
        _classify_begin_keyword(dVars, oLine)
        _classify_return_keyword(dVars, oLine)
        _classify_parameter(dVars, oLine)
        _classify_parameter_end(dVars, oLine)
        _classify_end_keyword(dVars, oLine)


def _classify_function_keyword(dVars, oLine):
    if re.match('^\s*function\s', oLine.lineLower) or re.match('^\s*impure\s', oLine.lineLower) or re.match('^\s*pure\s', oLine.lineLower):
        oLine.isFunctionKeyword = True
        oLine.insideFunction = True
        oLine.indentLevel = dVars['iCurrentIndentLevel']
        dVars['iCurrentIndentLevel'] += 1


def _classify_begin_keyword(dVars, oLine):
    if re.match('^\s*begin', oLine.lineLower):
        oLine.isFunctionBegin = True
        oLine.indentLevel = dVars['iCurrentIndentLevel'] - 1
        dVars['fFunctionBeginDetected'] = True

def _classify_return_keyword(dVars, oLine):
    if re.match('^\s*return', oLine.lineLower) and dVars['fFunctionBeginDetected']:
        oLine.isFunctionReturn = True
        oLine.indentLevel = dVars['iCurrentIndentLevel']

def _classify_is(dVars, oLine):
    if not dVars['fFunctionBeginDetected']:
        if oLine.has_token('is'):
            oLine.hasFunctionIs = True

def _classify_return_type(dVars, oLine):
    if oLine.has_token('return') and not dVars['fFunctionBeginDetected']:
        oLine.hasFunctionReturnType = True
        dVars['fFunctionReturnTypeDetected'] = True


def _classify_end_keyword(dVars, oLine):
    if oLine.insidePackage:
        if re.match('^.*return\s+\w+;', oLine.line, re.IGNORECASE):
            oLine.isFunctionEnd = True
            oLine.isFunctionReturn = True
            if re.match('^\s*return', oLine.line, re.IGNORECASE):
                oLine.indentLevel = dVars['iCurrentIndentLevel'] - 1
            if re.match('^\s*\)\s*return', oLine.line, re.IGNORECASE):
                oLine.indentLevel = dVars['iCurrentIndentLevel'] - 1
            dVars['iCurrentIndentLevel'] -= 1
            _clear_function_variables(dVars)
    else:
        if re.match('^\s*end', oLine.lineLower) and not oLine.isEndIfKeyword and \
           not oLine.isEndCaseKeyword and not oLine.isForLoopEnd and not oLine.isWhileLoopEnd and dVars['fFunctionBeginDetected']:
            oLine.isFunctionEnd = True
            oLine.indentLevel = dVars['iCurrentIndentLevel'] - 1
            dVars['iCurrentIndentLevel'] -= 1
            _clear_function_variables(dVars)

def _classify_parameter(dVars, oLine):
    if re.match('^.*\w+\s*:\s*\w+', oLine.line) and not dVars['fFunctionParameterEndDetected']:
        oLine.isFunctionParameter = True
        if not oLine.indentLevel:
            oLine.indentLevel = dVars['iCurrentIndentLevel']


def _classify_parameter_end(dVars, oLine):
    if ')' in oLine.line and dVars['iOpenParenthesis'] == dVars['iCloseParenthesis']:
        dVars['iOpenParenthesis'] = 0
        dVars['iCloseParenthesis'] = 0
        oLine.isFunctionParameterEnd = True
        if re.match('^\s*\)\s*is', oLine.line, re.IGNORECASE):
            oLine.indentLevel = dVars['iCurrentIndentLevel'] - 1
        dVars['fFunctionParameterEndDetected'] = True


def _clear_function_variables(dVars):
    dVars['fFunctionBeginDetected'] = False
    dVars['fFunctionParameterEndDetected'] = False
    dVars['fFunctionReturnTypeDetected'] = False

