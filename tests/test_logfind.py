import unittest
from logfind import *


class TestLogfind(unittest.TestCase):

    def test_if_o_present_in_command_line(self):
        self.assertEqual(is_o_present_in_command_line(['-o', 'abc', 'def']), True, "these are not the same")

    def test_if_o_is_absent_from_command_line(self):
        self.assertEqual(is_o_present_in_command_line(['abc', 'def']), False, "these are not the same")

    def test_regexpr_extraction_from_dot_file(self):
        """   
        This test will fail UNLESS you update 'list_of_regexprs' with the 
        """ 

        list_of_regexprs =  ['[a-zA-Z0-9\-\_\.]*']

        self.assertEqual(extract_regexprs_from_dot_logfind_file(".logfind"), list_of_regexprs, "not the same")

    def test_file_listing_in_directory(self):

        """
        This test will fail UNLESS you update 'list_of_files' with a list of files names in YOUR current working 
        directory. 
        """

        list_of_files = ['access_log', 'alphabets', 'alphabets_and_digits', 'apache_sample', 'arg.py', 'digits', 'error_log', 'logfind.py', 'test_logfind.py', '.logfind', 'test_logfind.py~', 'logfind.pyc', 'logfind.py~']

        self.assertEqual(set(obtain_list_of_files_in_directory()), set(list_of_files), "not the same")


if __name__ == '__main__':
    unittest.main()
