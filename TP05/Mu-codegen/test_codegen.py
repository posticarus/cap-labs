#! /usr/bin/env python3
import pytest
import glob
import os
import sys
import subprocess
import Main
from APICodeLEIA import AllocationError
import re

ALL_FILES = glob.glob('../tests/*.mu')

HERE = os.path.dirname(os.path.realpath(__file__))
TARGETM = os.path.join(HERE, '..', '..', '..', 'leia')
ASM = os.path.join(TARGETM, 'assembleur', 'asm.py')
SIMU = os.path.join(TARGETM, 'simulateur', 'LEIA')

MU_EVAL = os.path.join(
HERE, '..', '..', 'TP04', 'Mu-evalntype', 'Main.py')


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

    def naive_alloc(self, file):
        return self.compile_and_simulate(file, naive_alloc=True)

    def all_in_mem(self, file):
        return self.compile_and_simulate(file, all_in_mem=True)

    def remove(self, file):
        try:
            os.remove(file)
        except:
            pass

    def compile_and_simulate(self, file, naive_alloc=False, all_in_mem=False):
        basename, rest = os.path.splitext(file)
        print("Compiling ...")
        if naive_alloc:
            output_base = basename + '-naive'
        elif all_in_mem:
            output_base = basename + '-allinmem'
        else:
            output_base = basename
        output_name = output_base + '.s'
        self.remove(output_name)
        try:
            Main.main(file,
                      output_name=output_name,
                      naive_alloc=naive_alloc,
#                      three_addr=(naive_alloc or all_in_mem),
                      all_in_mem=all_in_mem)
        except AllocationError:
            if naive_alloc:
                return
            else:
                raise Exception("AllocationError should only happen "
                                "for naive_alloc=true")
        assert(os.path.isfile(output_name))
        print("Compiling ... OK")
        if naive_alloc or all_in_mem:  # Only executable code!
            sys.stderr.write("Assembling " + output_name + " ... ")
            self.remove(output_base + '.obj')
            cmd = [
                'python3', ASM, output_name,
                '-o', output_base + '.obj'
            ]
            subprocess.check_output(cmd)
            assert(os.path.isfile(output_base + '.obj'))
            sys.stderr.write("Assembling ... OK\n")
            try:
                return subprocess.check_output(
                    [SIMU, '-q', output_base + '.obj'],
                    timeout=10).decode("utf-8", "strict")
            except subprocess.TimeoutExpired:
                self.fail()
        else:
            return None

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
    def test_compile_and_simulate(self, filename):
        expect = self.get_expect(filename)
        actual = self.compile_and_simulate(filename)
        if expect and actual is not None:
            #  None: when simu has not been done.
            assert(actual == expect)

    @pytest.mark.parametrize('filename', ALL_FILES)
    def test_alloc(self, filename):
        expect = self.get_expect(filename)
        naive = self.naive_alloc(filename)
        if naive is not None:
            assert(naive == expect)
        mem = self.all_in_mem(filename)
        assert(mem == expect)


if __name__ == '__main__':
    pytest.main(sys.argv)
