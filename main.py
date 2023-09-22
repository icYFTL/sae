from core import Static
from source.parse import parse_from_file, parse_directives
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Hsf (Have some fun)')

    parser.add_argument('--input', '-i', required=True, help='Путь к входному файлу')
    parser.add_argument('--verbose', '-v', action='store_true', required=False, help='Выводить подробные сообщения')

    args = parser.parse_args()

    s = Static()


    def debug_print(debug=True):  # Xd im too lazy
        print('\n[DEBUG]' if debug else '\n[VALUES]')
        for i, reg in enumerate(s.REGS):
            print(f'REG{i}: {reg}')

        for i, mem in enumerate(s.MEMORY):
            print(f'mem_{i}: {mem}')
        print('[/DEBUG]\n' if debug else '[/VALUES]\n')


    print('### INITIAL VALUES')
    debug_print(False)

    print('### PARSE DIRECTIVES')

    directives = parse_directives(args.input)
    if directives:
        if directives.get('mem'):
            s.MEMORY = directives['mem']

    print('### PARSE BODY')
    pc = parse_from_file(args.input)
    print('### RUN')
    for command in pc:
        print(f'Running {command}')
        command.run()
        if args.verbose:
            debug_print()

    print('### RESULT VALUES')
    debug_print(False)
