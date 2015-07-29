#!/usr/bin/env python
from sys import argv, exit
from os.path import expanduser, isfile, join
from os import listdir
import sys
import re
import os


def is_empty(list_of_arguments):
    """
    This function checks for the absence of arguments (keywords) in the
    command line
    """
    if len(list_of_arguments) == 0:
        print """No keywords to search for"""
        exit(0)
    else:
        return


def get_match_type(arguments):
    """
    This function checks for the type of match operation to be performed.
    It returns either an 'AND' or an 'OR'
    """
    if arguments[0] == '-o':
        return "OR"
    else:
        return "AND"


def get_search_space():
    """
    This function reads the contents of .logfind (found in home directory,
    and returns lists of directories and their corresponding search patterns.
    """
    directories, patterns = [], []
    file_obj = open(expanduser("~") + "/.logfind")
    lines = file_obj.readlines()
    paths = map(lambda s: s.strip(), lines)
    for path in paths:
        l = path.split('/')
        patterns.append(l[-1])
        del l[0], l[-1]
        directories.append('/' + '/'.join(l))
    file_obj.close()
    return directories, patterns


def get_files(path):
    """
    This function returns a list of all files found in 'path'
    """
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    return onlyfiles


def get_files_matching_pattern(path, pattern):
    """
    Given a directory path and pattern, this function return a list
    of files that match 'pattern'
    """
    file_names = ' '.join(get_files(path))
    files_matching_pattern = re.findall(pattern, file_names)
    files_matching_pattern = [path + '/' + filename
                              for filename in
                              files_matching_pattern
                              if os.path.isfile(path + '/' + filename)]

    print "When the search space is set by", path + '/' + pattern, "\n"

    return files_matching_pattern


def match_OR(paths, patterns, arguments):
    """
    For a given search space (a list of files specified together
    by path and pattern) this function will report a match if one
    or more of the arguments are present in a single files. Mutliple
    matches are listed line by line
    """
    match = 0

    for path, pattern in zip(paths, patterns):

        for file in get_files_matching_pattern(path, pattern):

            file_object = open(file)
            content = file_object.read()

            for arg in arguments[1:]:
                if arg in content:
                    match = 1
                    print arg, "was found in", file, "\n"

            file_object.close()

        if match != 1:
            print "No match found."


def match_AND(paths, patterns, arguments):
    """
    For a given search space (a list of files specified together
    by path and pattern) this function will report a match if and only
    if all the arguments are present in a file
    """

    for path, pattern in zip(paths, patterns):

        for file in get_files_matching_pattern(path, pattern):

            file_object = open(file)
            content = file_object.read()
            matches = []

            for arg in arguments:
                if arg in content:
                    match = 1
                    matches.append(arg)
                else:
                    match = 0
                    break

            if match == 1:
                print matches, "found in", file, "\n"

            file_object.close()


def match(match_type, paths, patterns, arguments):
    """
    This is a wrapper function which calls either 'match_OR()' or
    'match_AND()' depending on the value of 'match_type'
    """

    if match_type == "OR":
        match_OR(paths, patterns, arguments)
    elif match_type == "AND":
        match_AND(paths, patterns, arguments)


if __name__ == '__main__':

    arguments = sys.argv[1:]
    is_empty(arguments)
    paths, patterns = get_search_space()
    match(get_match_type(arguments), paths, patterns, arguments)
