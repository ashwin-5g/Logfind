#!/usr/bin/env python
from sys import argv, exit
import os
import sys
import re


def extract_arguments_from_command_line():
    """
    This will extract all the arugments (typically strings) input by the
    user, and return these arguments in the form of a list. The function
    does not take in any arguments.
    """
    return sys.argv[1:]


def determine_if_list_of_arguments_is_empty(list_of_arguments):
    """
    This argument determines whether keyword(s) is(are) input by the user
    in the command line. If no keyword is found, then a msg is displayed.
    If there's one or more keywords to search for, execution of the rest
    of the program resumes.
    """
    if len(list_of_arguments) == 0:
        print """You have not input any keyword to search for. The program
will close now"""
        exit(0)
    else:
        return


def is_o_present_in_command_line(list_of_arguments):
    """
    This takes in a list of arguments input by the user, and determines if
    '-o' is one of the arguments. The function returns a boolean value.
    """
    if list_of_arguments[0] == '-o':
        return True
    else:
        return False


def extract_regexprs_from_dot_logfind_file(dotfile_path):
    """
    This function reads the contents of the .logfind file, extracts the
    regular expressions specified (by the user), and returns these in the
    form of a list.
    """
    dotfile_object = open(dotfile_path)
    lines = dotfile_object.readlines()
    list_of_regexprs = map(lambda s: s.strip(), lines)
    dotfile_object.close()
    return list_of_regexprs


def obtain_list_of_files_in_directory():
    """
    This function builds a list of all files (files ONLY)
    in the current working directory and returns them.
    """
    list_of_all_directories_and_files = os.listdir(os.getcwd())
    list_of_files_in_directory = [f for f in list_of_all_directories_and_files
                                  if os.path.isfile(os.getcwd() + '/' + f)]
    return list_of_files_in_directory


def obtain_list_of_file_paths_matching_regexpr(regexpr):
    """
    Given a regular expression (obtained from .logfind) as input, this
    function will return a list of files (specified by their complete set
    of paths) based entirely on the regular expression.
    """
    string_of_file_names = ' '.join(obtain_list_of_files_in_directory())
    files_matching_regexpr = re.findall(regexpr, string_of_file_names)
    list_of_file_paths_matching_regexpr = [os.getcwd() + '/' + filename
                                           for filename in
                                           files_matching_regexpr
                                           if os.path.isfile(os.getcwd() + '/' + filename)]

    print "When the search space is set by the", regexpr, "pattern: ", "\n"
    return list_of_file_paths_matching_regexpr


def match_when_o_is_present_in_command_line(list_of_files_matching_regexpr,
                                            list_of_arguments):
    """
    This function takes in two arguments: first, a list of files
    that matches a particular reg expr; second, a list of command line
    arguments which will be "looked for" in the contents of the set of
    above-mentioned list of files. The 'o' dicates that a match is made when
    if one or more of the arguments is found in a given file.

    When a successful match is made, the argument is reported to have
    been found in a given file.

    When a match is unsuccessful (i.e., when none of the list of arguments
    are found in any of the files), the message "no match found" is displayed.
    """
    match = 0
    for path in list_of_files_matching_regexpr:

        file_object = open(path)
        content = file_object.read()

        for arg in list_of_arguments[1:]:
            if arg in content:
                match = 1
                print arg, "was found in", path, "\n"

        file_object.close()

    if match != 1:
        print "No match found."


def match_when_o_is_absent_from_command_line(list_of_files_matching_regexpr,
                                             list_of_arguments):
    """
    This function takes in two arguments: first, a list of files
    that match a particular reg expr; second, a list of command line
    arguments which will be "looked for" in the the contents of the set of
    above-mentioned list of files. The *absence* of 'o' in the command line
    argument dictates that a match is made IF and ONLY IF ALL of the arguments
    are found in a given file.

    When a successful match is made, the argument(s) is(are) reported to have
    been found in a given file.

    When a match is unsuccessful (i.e., if even one among the list of
    arguments is NOT found in any of the files), the message "no match found"
    is displayed.
    """
    for path in list_of_files_matching_regexpr:

        file_object = open(path)
        content = file_object.read()
        matches = []

        for arg in list_of_arguments:
            if arg in content:
                match = 1
                matches.append(arg)
            else:
                match = 0
                break

        if match == 1:
            print matches, "found in", path, "\n"

        file_object.close()

if __name__ == '__main__':

    if '.logfind' not in obtain_list_of_files_in_directory():
        print """Make sure you include the .logfind file in your current working directory. Also
specify one or more regular expressions in this file in the manner instructed in the README"""

    else:
        list_of_regexprs = extract_regexprs_from_dot_logfind_file(".logfind")

        list_of_arguments = extract_arguments_from_command_line()

        determine_if_list_of_arguments_is_empty(list_of_arguments)

        for regexpr in list_of_regexprs:

            list_of_files_matching_regexpr = obtain_list_of_file_paths_matching_regexpr(regexpr)

            if is_o_present_in_command_line(list_of_arguments):
                match_when_o_is_present_in_command_line(list_of_files_matching_regexpr,
                                                        list_of_arguments)
            else:
                match_when_o_is_absent_from_command_line(list_of_files_matching_regexpr, list_of_arguments)
