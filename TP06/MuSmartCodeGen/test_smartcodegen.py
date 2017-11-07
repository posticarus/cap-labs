#! /usr/bin/env python3
import pytest
import glob
import os
import sys
import subprocess
import Main
from APICodeLEIA import AllocationError
import re

ALL_FILES = glob.glob("tests/*.mu")

#ALL_FILES = glob.glob('testsregandspill/*.mu')+glob.glob("tests/*.mu")\
#+glob.glob("testsconflictgraph/*.mu")+glob.glob('testsdataflow/*.mu')

HERE = os.path.dirname(os.path.realpath(__file__))
TARGETM = os.path.join(HERE, '..', '..', 'leia')
ASM = os.path.join(TARGETM, 'assembleur', 'asm.py')
SIMU = os.path.join(TARGETM, 'simulateur', 'LEIA')
MU_EVAL = os.path.join(
    HERE, '..', '..', 'TP04', 'code', 'Mu-evalntype', 'Main.py')


class TestCodeGen(object):
    __expect = {}

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

    def evaluate(self, file):
        return subprocess.check_output([
            'python3',
            MU_EVAL,
            file]).decode("utf-8", "strict")

    def smart_alloc(self, file):
        return self.compile_and_simulate(file)

    def remove(self, file):
        try:
            os.remove(file)
        except:
            pass

    def compile_and_simulate(self, file):
        basename, rest = os.path.splitext(file)
        print("Compiling (smart alloc) ...")
        output_name = basename + '.s'
        self.remove(output_name)
        try:
            Main.main(file)
        except AllocationError:
            raise Exception("AllocationError should not happen!")
        assert(os.path.isfile(output_name))
        print("Compiling ... OK")
        sys.stderr.write("Assembling " + output_name + " ... ")
        self.remove(basename + '.obj')
        cmd = [
            'python3', ASM, output_name,
            '-o', basename + '.obj'
        ]
        subprocess.check_output(cmd)
        assert(os.path.isfile(basename + '.obj'))
        sys.stderr.write("Assembling ... OK\n")
        try:
            return subprocess.check_output(
                [SIMU, '-q', basename + '.obj'],
                timeout=10).decode("utf-8", "strict")
        except subprocess.TimeoutExpired:
            self.fail()

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

    @pytest.mark.parametrize('filename', ALL_FILES)
    def test_alloc(self, filename):
        expect = self.get_expect(filename)
        alloc = self.smart_alloc(filename)
        if alloc is not None:
            assert(alloc == expect)


if __name__ == '__main__':
    pytest.main(sys.argv)
