import re


def concurrent(dVars, oLine):
    if not (oLine.insideArchitecture and not oLine.insideProcess):
        return
    if re.match('^\s*\w+.*\s*<=', oLine.lineNoComment):
        if not oLine.insideAssert and not oLine.insideConcurrent:
            oLine.indentLevel = dVars['iCurrentIndentLevel']
            oLine.isConcurrentBegin = True
            oLine.insideConcurrent = True
            if re.match('^\s*\w+\s*:\s*\w+.*\s*<=', oLine.lineNoComment):
                oLine.hasConcurrentLabel = True
    if oLine.insideConcurrent:
        if re.match('.*;', oLine.lineNoComment):
            oLine.isEndConcurrent = True
