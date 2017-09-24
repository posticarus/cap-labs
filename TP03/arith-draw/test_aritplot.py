#! /usr/bin/env python3
"""
Testing script for TP3 (aritplot mini-project)
Usage:
    python3 test_aritplot.py
"""


import unittest
import fnmatch
import os
import re
import io
from contextlib import redirect_stdout

import arit

HERE = os.path.dirname(os.path.realpath(__file__))


class TestAritEval(unittest.TestCase):
    def test_ex(self):
        self.all_files_in_dir(os.path.join(HERE, 'ex'))

    def all_files_in_dir(self, dir):
        for file in os.listdir(dir):
            path = os.path.join(dir, file)
            if fnmatch.fnmatch(file, '*.txt'):
                with self.subTest(msg=path):
                    self.one_file(path)

    def extract_expect(self, file):
        inside_expected = False
        expected_lines = []
        with open(file, encoding="utf-8") as f:
            for line in f.readlines():
                # Ignore non-comments
                if not re.match('\s*#', line):
                    continue
                # Cleanup comment start and whitespaces
                line = re.sub('\s*#\s*', '', line)
                line = re.sub('\s*$', '', line)

                if line == 'END EXPECTED':
                    inside_expected = False

                if inside_expected:
                    expected_lines.append(line)

                if line == 'EXPECTED':
                    inside_expected = True

        expected_lines.append('')
        return '\n'.join(expected_lines)

    def remove(self, file):
        try:
            os.remove(file)
        except OSError:
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
        expect = self.extract_expect(file)
        actual = self.execute(file)
        if expect:
            self.assertEqual(actual, expect)

if __name__ == '__main__':
    unittest.main() # runs TestAritEval.test_ex()
