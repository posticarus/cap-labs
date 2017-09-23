#! /usr/bin/env python3
"""
Testing script for TP3 (aritplot mini-project)
Usage:
    python3 test_aritplot.py
"""


import unittest
import fnmatch
import os
import arit
import re
import io

from contextlib import redirect_stdout

HERE = os.path.dirname(os.path.realpath(__file__))


class TestAritEval(unittest.TestCase):
    def test_ex(self):
        self.all_files_in_dir(os.path.join(HERE, 'ex'))

    def all_files_in_dir(self, dir):
        for file in os.listdir(dir):
            if fnmatch.fnmatch(file, '*.txt'):
                self.one_file(os.path.join(dir, file))

    def extract_expect(self, file):
        state = 'outside'
        result = ''
        with open(file, encoding="utf-8") as f:
            for line in f.readlines():
                # Ignore non-comments
                if not re.match('\s*#', line):
                    continue
                # Cleanup comment start and whitespaces
                line = re.sub('\s*#\s*', '', line)
                line = re.sub('\s*$', '', line)

                if line == 'END EXPECTED':
                    state = 'outside'

                if state == 'inside_expected':
                    result += line + '\n'

                if line == 'EXPECTED':
                    state = 'inside_expected'
        return result

    def remove(self, file):
        try:
            os.remove(file)
        except:
            pass

    def execute(self, file):
        basename, rest = os.path.splitext(file)
        output_name = basename + '.res'
        self.remove(output_name)
        f = io.StringIO()
        # redirection of stdout to an output file
        with redirect_stdout(f):
            arit.main(file, False)
        return f.getvalue()

    def one_file(self, file):
        print("analysing "+file)
        expect = self.extract_expect(file)
        print(expect)
        actual = self.execute(file)
        print(actual)
        print("Result for", file)
        if expect:
            self.assertEqual(actual, expect)
        print(file, ": OK")

if __name__ == '__main__':
    unittest.main()
