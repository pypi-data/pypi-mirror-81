#!/usr/bin/env python

import argparse
import sys
import os
import json
import shutil
import glob
import yaml

from . import junit
from . import rule_list
from . import severity
from . import version
from . import vhdlFile


def parse_command_line_arguments():
    '''Parses the command line arguments and returns them.'''

    parser = argparse.ArgumentParser(
      prog='VHDL Style Guide (VSG)',
      description='''Analyzes VHDL files for style guide violations.
                   Reference documentation is located at:
                   http://vhdl-style-guide.readthedocs.io/en/latest/index.html''')

    parser.add_argument('-f', '--filename', nargs='+', help='File to analyze')
    parser.add_argument('-lr', '--local_rules', help='Path to local rules')
    parser.add_argument('-c', '--configuration', nargs='+', help='JSON or YAML configuration file(s)')
    parser.add_argument('--fix', default=False, action='store_true', help='Fix issues found')
    parser.add_argument('-fp', '--fix_phase', default=10, action='store', help='Fix issues up to and including this phase')
    parser.add_argument('-j', '--junit', action='store', help='Extract Junit file')
    parser.add_argument('-of', '--output_format', action='store', default='vsg', choices=['vsg', 'syntastic'], help='Sets the output format.')
    parser.add_argument('-b', '--backup', default=False, action='store_true', help='Creates a copy of input file for comparison with fixed version.')
    parser.add_argument('-oc', '--output_configuration', default=None, action='store', help='Write configuration to file name.')
    parser.add_argument('-rc', '--rule_configuration', default=None, action='store', help='Display configuration of a rule')
    parser.add_argument('--style', action='store', default=None, choices=get_predefined_styles(), help='Use predefined style')
    parser.add_argument('-v', '--version', default=False, action='store_true', help='Displays version information')
    parser.add_argument('--debug', default=False, action='store_true', help='Displays verbose debug information')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    else:
        return parser.parse_args()


def get_predefined_styles():
    '''
    Reads all predefined styles and returns a list of names.

    Parameters : None

    Returns : (list of strings)
    '''
    lReturn = []
    sStylePath = os.path.join(os.path.dirname(__file__), 'styles')
    lStyles = os.listdir(sStylePath)
    for sStyle in lStyles:
        if sStyle.endswith('.yaml'):
            with open(os.path.join(sStylePath, sStyle)) as yaml_file:
                tempConfiguration = yaml.full_load(yaml_file)
            lReturn.append(tempConfiguration['name'])
    return lReturn


def read_predefined_style(sStyleName):
    '''
    Reads a predefined style file.

    Parameters :

      sStyleName : (string)

    Returns : (dictionary)
    '''
    dReturn = {}
    if sStyleName is not None:
        sFileName = os.path.join(os.path.dirname(__file__), 'styles', sStyleName + '.yaml')
        dReturn = open_configuration_file(sFileName)
    return dReturn
    

def open_configuration_file(sFileName, sJUnitFileName=None):
    '''Attempts to open a configuration file and read it's contents.'''
    try:
        with open(sFileName) as yaml_file:
            tempConfiguration = yaml.full_load(yaml_file)
    except IOError:
        print('ERROR: Could not find configuration file: ' + sFileName)
        write_invalid_configuration_junit_file(sFileName, sJUnitFileName)
        sys.exit(1)
    except yaml.scanner.ScannerError as e:
        print('ERROR: Invalid configuration file: ' + sFileName)
        print(e)
        write_invalid_configuration_junit_file(sFileName, sJUnitFileName)
        exit()
    except yaml.parser.ParserError as e:
        print('ERROR: Invalid configuration file: ' + sFileName)
        print(e)
        write_invalid_configuration_junit_file(sFileName, sJUnitFileName)
        exit()
    return tempConfiguration


def validate_file_exists(sFilename, sConfigName):
    '''Validates a file exist while using the glob function to expand filenames.'''
    if isinstance(sFilename, dict):
        sExpandedFilename = list(sFilename.keys())[0]
    else:
        sExpandedFilename = sFilename
    lFileNames = glob.glob(expand_filename(sExpandedFilename))
    if len(lFileNames) == 0:
        print('ERROR: Could not find file ' + sFilename + ' in configuration file ' + sConfigName)
        sys.exit(1)


def read_configuration_files(dStyle, commandLineArguments):
    dConfiguration = dStyle
    if commandLineArguments.configuration:
        for sConfigFilename in commandLineArguments.configuration:
            try:
                tempConfiguration = open_configuration_file(sConfigFilename, commandLineArguments.junit)
            except AttributeError:
                tempConfiguration = open_configuration_file(sConfigFilename)


            for sKey in tempConfiguration.keys():
                if sKey == 'file_list':
                    if 'file_list' not in dConfiguration:
                        dConfiguration['file_list'] = []
                    for iIndex, sFilename in enumerate(tempConfiguration['file_list']):
                        validate_file_exists(sFilename, sConfigFilename)
                        try:
                            for sGlobbedFilename in glob.glob(expand_filename(sFilename)):
                                dConfiguration['file_list'].append(sGlobbedFilename)
                        except TypeError:
                            sKey = list(sFilename.keys())[0]
                            for sGlobbedFilename in glob.glob(expand_filename(sKey)):
                                dTemp = {}
                                dTemp[sGlobbedFilename] = {}
                                dTemp[sGlobbedFilename].update(tempConfiguration['file_list'][iIndex][sKey])
                                dConfiguration['file_list'].append(dTemp)

                elif sKey == 'rule':
                    for sRule in tempConfiguration[sKey]:
                        try:
                            dConfiguration[sKey][sRule] = tempConfiguration[sKey][sRule]
                        except:
                            dConfiguration[sKey] = {}
                            dConfiguration[sKey][sRule] = tempConfiguration[sKey][sRule]
                else:
                    dConfiguration[sKey] = tempConfiguration[sKey]

    return dConfiguration


def write_invalid_configuration_junit_file(sFileName, sJUnitFileName):
    if sJUnitFileName:
        oJunitFile = junit.xmlfile(sJUnitFileName)
        oJunitTestsuite = junit.testsuite('vhdl-style-guide', str(0))
        oJunitTestcase = junit.testcase(sFileName, str(0), 'failure')
        oFailure = junit.failure('Failure')
        oFailure.add_text('Invalid JSON format.  Review configuration for errors.')
        oJunitTestcase.add_failure(oFailure)
        oJunitTestsuite.add_testcase(oJunitTestcase)
        oJunitFile.add_testsuite(oJunitTestsuite)
        write_junit_xml_file(oJunitFile)


def write_vhdl_file(oVhdlFile):
    try:
        with open(oVhdlFile.filename, 'w') as oFile:
            for oLine in oVhdlFile.lines[1:]:
                oFile.write(oLine.line + '\n')
    except PermissionError as err:
        print (err, "Could not write fixes back to file.")


def write_junit_xml_file(oJunitFile):
    with open(oJunitFile.filename, 'w') as oFile:
        for sLine in oJunitFile.build_junit():
            oFile.write(sLine + '\n')


def update_command_line_arguments(commandLineArguments, configuration):

    if 'skip_phase' in configuration:
        commandLineArguments.skip_phase = configuration['skip_phase']
    else:
        commandLineArguments.skip_phase = []

    if not configuration:
        return

    if 'file_list' in configuration:
        for sFilename in configuration['file_list']:
            if isinstance(sFilename, dict):
                sFilename = list(sFilename.keys())[0]
            try:
                commandLineArguments.filename.extend(glob.glob(expand_filename(sFilename)))
            except:
                commandLineArguments.filename = glob.glob(expand_filename(sFilename))
    if 'local_rules' in configuration:
        commandLineArguments.local_rules = expand_filename(configuration['local_rules'])


def expand_filename(sFileName):
    '''Expands environment variables in filenames.'''
    return os.path.expanduser(os.path.expandvars(sFileName))


def create_backup_file(sFileName):
    '''Copies existing file and adds .bak to the end.'''
    shutil.copy2(sFileName, sFileName + '.bak')


def read_vhdlfile(sFileName):
    try:
        lLines = []
        with open(sFileName) as oFile:
            for sLine in oFile:
                lLines.append(sLine)
        oFile.close()
        return lLines
    except IOError:
        return []


def generate_output_configuration(commandLineArguments, configuration):
    '''
    Creates a configuration based on parameters passed on the command line.
    It will send the output to a file in JSON format.

    Parameters:

      commandLineArguments: (argparse object)

      configuration: (configuration dictionary)

    Returns:  Nothing
    '''
    if commandLineArguments.output_configuration:
        fExitStatus = 0
        # Create empty file so it can be used to create the rule list
        oVhdlFile = vhdlFile.vhdlFile([''])
        oRules = rule_list.rule_list(oVhdlFile, configuration['severity_list'], commandLineArguments.local_rules)
        oRules.configure(configuration)
        dOutputConfiguration = {}
        dOutputConfiguration['cwd'] = os.getcwd()
        if commandLineArguments.filename:
            dOutputConfiguration['file_list'] = []
            for sFileName in commandLineArguments.filename:
                dOutputConfiguration['file_list'].append(sFileName)
        if commandLineArguments.local_rules:
            dOutputConfiguration['local_rules'] = commandLineArguments.local_rules
        dOutputConfiguration['rule'] = oRules.get_configuration()
        with open(commandLineArguments.output_configuration, 'w') as json_file:
            json.dump(dOutputConfiguration, json_file, sort_keys=True, indent=2)
        sys.exit(fExitStatus)


def display_rule_configuration(commandLineArguments, configuration):
    '''
    Displays the configuration of a rule passed on the command line.

    Parameters:

      commandLineArguments: (argparse object)

      configuration: (configuration dictionary)

    Returns:  Nothing
    '''
    if commandLineArguments.rule_configuration:
        fExitStatus = 0
        # Create empty file so it can be used to create the rule list
        oVhdlFile = vhdlFile.vhdlFile([''])
        oRules = rule_list.rule_list(oVhdlFile, configuration['severity_list'], commandLineArguments.local_rules)
        oRules.configure(configuration)
        dOutputConfiguration = {}
        if commandLineArguments.local_rules:
            dOutputConfiguration['local_rules'] = commandLineArguments.local_rules
        dFullConfiguration = oRules.get_configuration()
        if commandLineArguments.rule_configuration in dFullConfiguration:
            dOutputConfiguration['rule'] = {}
            dOutputConfiguration['rule'][commandLineArguments.rule_configuration] = dFullConfiguration[commandLineArguments.rule_configuration]
            # Format the data for displaying
            print(json.dumps(dOutputConfiguration, indent=2))
        else:
            print('ERROR: rule ' + commandLineArguments.rule_configuration + ' was not found.')
            fExitStatus = 1
        sys.exit(fExitStatus)


def validate_files_exist_to_analyze(sName):
    if sName == None:
        print('ERROR: No file defined by the -f command line option or filename given in configuration file.')
        sys.exit(1)


def add_debug_to_configuration(oCLA, dConfiguration):
    '''
    Adds debug values to the configuration dictionary for later use.

    Parameters:

      oCLA: (command line argument object)

      dConfiguration: (dictionary)

    Returns:  Nothing
    '''
    try:
        dConfiguration['debug'] = oCLA.debug
    except TypeError:
        dConfiguration = {}
        dConfiguration['debug'] = oCLA.debug
    return dConfiguration


def main():
    '''Main routine of the VHDL Style Guide (VSG) program.'''

    fExitStatus = 0

    commandLineArguments = parse_command_line_arguments()

    version.print_version(commandLineArguments)

    dStyle = read_predefined_style(commandLineArguments.style)

    configuration = read_configuration_files(dStyle, commandLineArguments)

    update_command_line_arguments(commandLineArguments, configuration)

    configuration = add_debug_to_configuration(commandLineArguments, configuration)

    # Add local rule path to system path so the rules can be loaded
    if commandLineArguments.local_rules:
        sys.path.append(os.path.abspath(commandLineArguments.local_rules))

    if commandLineArguments.junit:
        oJunitFile = junit.xmlfile(commandLineArguments.junit)
        oJunitTestsuite = junit.testsuite('vhdl-style-guide', str(0))

    oSeverityList = severity.create_list(configuration)
    configuration['severity_list'] = oSeverityList

    generate_output_configuration(commandLineArguments, configuration)

    display_rule_configuration(commandLineArguments, configuration)

    validate_files_exist_to_analyze(commandLineArguments.filename)

    for iIndex, sFileName in enumerate(commandLineArguments.filename):
        oVhdlFile = vhdlFile.vhdlFile(read_vhdlfile(sFileName))
        oVhdlFile.filename = sFileName
        oRules = rule_list.rule_list(oVhdlFile, oSeverityList, commandLineArguments.local_rules)
        oRules.configure(configuration)
        try:
            oRules.configure(configuration['file_list'][iIndex][sFileName])
        except TypeError:
            pass
        except KeyError:
            pass

        if commandLineArguments.fix:
            if commandLineArguments.backup:
                create_backup_file(sFileName)
            oRules.fix(commandLineArguments.fix_phase, commandLineArguments.skip_phase)
            write_vhdl_file(oVhdlFile)

        oRules.oSeverityList.clear_severity_counts()
        oRules.clear_violations()
        oRules.check_rules(commandLineArguments.skip_phase)
        oRules.report_violations(commandLineArguments.output_format)
        fExitStatus = update_exit_status(fExitStatus, oRules)

        if commandLineArguments.junit:
            oJunitTestsuite.add_testcase(oRules.extract_junit_testcase(sFileName))

    if commandLineArguments.junit:
        oJunitFile.add_testsuite(oJunitTestsuite)
        write_junit_xml_file(oJunitFile)


    sys.exit(fExitStatus)


def update_exit_status(fExitStatus, oRules):
    if fExitStatus == 1 or oRules.violations:
        return 1
    else:
        return 0

if __name__ == '__main__':
    main()
