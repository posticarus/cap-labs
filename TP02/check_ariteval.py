import re
import os
import sys
import subprocess

def debug(*args):
    """Like print(), but on stderr."""
    print(*args, file=sys.stderr)

def parse_specifications():
    """Parse the LaTeX file of the course to use as an example input
    and output."""
    tex = os.path.join(os.path.dirname(__file__), '..', 'tp2.tex')

    spec_input = []
    spec_output = []

    # To parse lines of line this one: {\tt 1;} & 1 = 1 \\
    pattern = re.compile(r'^{\\tt (?P<input>.*;)} & (?P<output>.*) \\\\')

    with open(tex) as fd:
        # Iterate trough lines until the BEGIN marker is found
        for line in fd:
            if line == '% BEGIN AUTOTEST ARIT\n':
                # Everything before this marker is ignored.
                break
        else:
            print('spec not found')
            exit(1)

        for line in fd:
            match = pattern.match(line)
            if line == '% END AUTOTEST ARIT\n':
                # Everything after this marker is ignored
                break
            if match:
                # This is a specification line, add it to the spec.
                spec_input.append(match.group('input'))
                spec_output.append(match.group('output'))

    debug('Got {} specifications'.format(len(spec_input)))
    return (spec_input, spec_output)

def run_code(input_, code_path):
    """Runs the code to be tested and returns its output. Pipes its
    stderr to this process' stderr."""
    # Compile the tested code.
    subprocess.check_output(['make', '-C', code_path])

    debug()
    debug()
    debug('stderr:')

    # Run the tested code, send it the input, and get its output.
    output = subprocess.check_output(
            ['make', 'run', '--silent', '-C', code_path],
            input='\n'.join(input_),
            universal_newlines=True,
            )
    debug()
    return output

def normalize_line(line):
    """Removes whitespaces."""
    return line.strip().replace(' ', '')

def count_mistakes(inputs, expected_outputs, outputs):
    """Compares intput and output, and counts the number of lines that
    are not equal (modulo normalization)."""
    nb_mistakes = 0

    # Iterate through each line of the expected/actual outputs,
    # and compare them with each other.
    for (input_line, expected, got) in zip(inputs, expected_outputs, outputs):
        if normalize_line(expected) == normalize_line(got):
            debug('{} ok'.format(input_line))
        else:
            nb_mistakes += 1
            debug('{}\n\texpected\t{!r}\n\tgot     \t{!r}'.format(input_line, expected, got))

    return nb_mistakes

def check_specifications(code_path):
    """Runs the code on the inputs in the specification (ie. tp2.pdf) and
    compare them with the associated outputs."""
    (spec_input, spec_output) = parse_specifications()
    output = run_code(spec_input, code_path)
    debug()
    debug('Checking specifications:')
    debug()

    return count_mistakes(spec_input, spec_output, output.split('\n'))


def parse_test_file(test_file):
    """Reads a .txt file in the format explained when using
    'python3 check_ariteval.py --help'."""
    inputs = []
    outputs = []
    with open(test_file) as fd:
        for line in fd:
            line = line.strip()
            if '#' not in line:
                continue # Ignore lines without a #
            (in_, out) = line.split('#')
            inputs.append(in_.strip())
            outputs.append(out.strip())

    return (inputs, outputs)

def check_test_file(test_file, code_path):
    """Runs the code on the inputs in a test file (see the explainations
    with 'python3 check_ariteval.py --help) and compare them with the
    associated outputs."""
    (test_input, test_output) = parse_test_file(test_file)
    output = run_code(test_input, code_path)
    debug()
    debug('Checking test file {}:'.format(test_file))
    debug()

    return count_mistakes(test_input, test_output, output.split('\n'))

def all_checks(code_path, test_files):
    """Runs specification checks and test file checks, counts their errors,
    and return a list that can be used as the final CSV line."""
    csv_line = [code_path]

    try:
        nb_mistakes_in_spec = check_specifications(code_path)
        debug()
        debug('{} mistakes in specification.'.format(nb_mistakes_in_spec))
        csv_line.append(nb_mistakes_in_spec)
    except FileNotFoundError:
        csv_line.append('NA')

    for test_file in test_files:
        nb_mistakes = check_test_file(test_file, code_path)
        debug()
        debug('{}: {} mistakes'.format(test_file, nb_mistakes))
        csv_line.append(nb_mistakes)

    debug()
    return csv_line

def main():
    if set(sys.argv) & {'-h', '-help', '--h', '--help'}:
        print('Syntax: {} path/to/code [path/to/testfile1 [path/to/testfile2 [...]]'
                .format(sys.argv[0]))
        print()
        print('path/to/code should contain a Makefile with a "run" target '
              'that runs an interpreter of AritEval.')
        print()
        print('path/to/testfile1 should be a file following this format:')
        print()
        print('\tinput expression1 # expected output1')
        print('\tinput expression2 # expected output2')
        print('\t...')
        print()
        print('For instance:')
        print()
        print('\t20 + 22; # 20 + 22 = 42')
        print('\ta = 4; # a now equals 4')
        print('\ta + 2; # a + 2 = 6')
        print('\ta * 5; # a * 5 = 20')
        print()
        print('When comparing the expected output with the actual output, '
              'whitespaces are stripped to avoid silly false negatives.')
        return
    try:
        (_, code_path, *test_files) = sys.argv
    except ValueError:
        print('Syntax: {} path/to/code [path/to/testfile1 [path/to/testfile2 [...]]'
                .format(sys.argv[0]))
        exit(1)

    csv_line = all_checks(code_path, test_files)
    print(','.join(map(str, csv_line)))

if __name__ == '__main__':
    main()
