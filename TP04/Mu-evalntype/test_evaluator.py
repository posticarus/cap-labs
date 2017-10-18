#! /usr/bin/env python3
import pytest
import glob
import os
import sys
import subprocess
import re
import collections

# ALL_FILES = glob.glob('../ex/*.mu')
# test all files in ex
# ALL_FILES = glob.glob('../ex/bad_*.mu')
# only test programs with runtime or typing error
#ALL_FILES = glob.glob('../ex/test*.mu')
# only test programs with no expected error (test*.mu)

ALL_FILES = glob.glob('../ex/eleves/*/*.mu')

if 'TEST_FILES' in os.environ:
    ALL_FILES = glob.glob(os.environ['TEST_FILES'])

HERE = os.path.dirname(os.path.realpath(__file__))

MU_EVAL = os.path.join(HERE, 'Main.py')

testresult = collections.namedtuple('testresult', ['exitcode', 'output'])

class TestCodeGen(object):
    __expect = {}

    def extract_expect(self, file):
        exitcode = 0
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
                elif line.startswith('EXITCODE'):
                    exitcode = int(line.split(' ')[1])
                elif line == 'EXPECTED':
                    inside_expected = True
                elif inside_expected:
                    expected_lines.append(line)

        expected_lines.append('')
        return testresult(exitcode=exitcode, output='\n'.join(expected_lines))

    def evaluate(self, file):
        try:
            output = subprocess.check_output(['python3', MU_EVAL, file])
            exitcode = 0
        except subprocess.CalledProcessError as e:
            output = e.output
            exitcode = e.returncode
        return testresult(exitcode=exitcode, output=output.decode())

    def remove(self, file):
        try:
            os.remove(file)
        except:
            pass

    @pytest.mark.parametrize('filename', ALL_FILES)
    def test_expect(self, filename):
        expect = self.extract_expect(filename)
        eval = self.evaluate(filename)
        if expect:
            assert(expect == eval)
        self.__expect[filename] = eval

    def get_expect(self, filename):
        if filename not in self.__expect:
            self.test_expect(filename)
        return self.__expect[filename]


if __name__ == '__main__':
    pytest.main(sys.argv)
