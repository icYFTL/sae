from core import Static
from source.parse import parse_text_from_file, parse_binary_from_file, parse_directives
import argparse
from source.command import *
from source.command.base_logic_command import BaseLogicCommand

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Hsf (Have some fun)')

    parser.add_argument('--input', '-i', required=True, help='Путь к входному файлу')
    parser.add_argument('--verbose', '-v', action='store_true', required=False, help='Выводить подробные сообщения')
    parser.add_argument('--mode', '-m', required=True, help='Режим работы text|binary')

    args = parser.parse_args()

    s = Static()


    def debug_print(debug=True):  # Xd im too lazy
        print('\n[DEBUG]' if debug else '\n[VALUES]')
        for i, reg in enumerate(s.REGS):
            print(f'REG{i}: {reg}')

        for i, mem in enumerate(s.MEMORY):
            print(f'mem_{i}: {mem}')
        print('[/DEBUG]\n' if debug else '[/VALUES]\n')


    def find_loop_by_name(commands, loop_name, loop_type=AwhileCommand):
        for i, cmd in enumerate(commands):
            if isinstance(cmd, loop_type):
                if cmd.name == loop_name:
                    return i, cmd

        raise RuntimeError(f'Can\'t find loop with name {loop_name} and type {loop_type}')


    print('### INITIAL VALUES')
    debug_print(False)

    print('### PARSE DIRECTIVES')

    directives = parse_directives(args.input)
    if directives:
        if directives.get('mem'):
            s.MEMORY = directives['mem']

    print('### PARSE BODY')
    if args.mode == 'text':
        pc = parse_text_from_file(args.input)
    elif args.mode == 'binary':
        pc = parse_binary_from_file(args.input)
    else:
        raise ValueError(f'Invalid mode passed. Wanted: text|binary, Got: {args.mode}')
    print('### RUN')
    loop_inst = None
    i = 0
    while True:
        command = pc[i]
        print(f'Running {command}')
        # if isinstance(command, AwhileCommand):
        #     result = command.run()
        #     if not result:
        #         raise RuntimeError('Xdxd')
        #     loop_inst = command, i
        #     i += 1
        #     continue
        if issubclass(command.__class__, BaseLogicCommand):
            result = command.run()
            if result[0] is True:
                i = result[1]
                continue
            else:
                if i == len(pc) - 1:
                    break
                i += 1
                continue

        command.run()

        if args.verbose:
            debug_print()

        i += 1
        if i >= len(pc):
            break

    print('### RESULT VALUES')
    debug_print(False)
