import os
import importlib
import re

from core import Static
from source.utils import get_reg_by_code, get_reg_by_name
from source.command import *

s = Static()


def parse_directives(filepath):
    with open(filepath, 'r', encoding='UTF-8') as f:
        raw = f.read()
        if raw:
            if raw.split('\n')[0].startswith('--'):
                r = re.findall(r'--mem=\[.*\]', raw.split('\n')[0])
                if r:
                    print('Found --mem directive')
                    l = raw.split('\n')[0].split('=')[-1].replace(';', '')
                    try:
                        baked_mem = eval(l)
                        return {'mem': baked_mem}
                    except:
                        raise RuntimeError('Invalid --mem directive\'s value')
                else:
                    print(f'Unknown {raw[0]} directive, skipped')


def get_command_from_bin(raw_code):
    global s
    raw_code = str(raw_code)
    cmd_type = bin(int(raw_code[:4], 2))[2:].zfill(4)  # 31-28
    literal = bin(int(raw_code[4:20], 2))[2:].zfill(16)  # 27-12
    dest = bin(int(raw_code[20:24], 2))[2:].zfill(4)  # 11-8
    op1 = bin(int(raw_code[24:28], 2))[2:].zfill(4)  # 7-4
    op2 = bin(int(raw_code[28:32], 2))[2:].zfill(4)  # 3-0

    reg1 = get_reg_by_code(op1)
    reg2 = get_reg_by_code(op2)
    dest_reg = get_reg_by_code(dest)

    src = int(literal, 2)

    files = os.listdir('source/command')

    python_files = [file for file in files if
                    file.endswith('.py') and not file.startswith('base') and not file.startswith('__')]

    for python_file in python_files:
        module_name = python_file[:-3]

        command = importlib.import_module(f'source.command.{module_name}')
        class_name = ''.join([x.capitalize() for x in module_name.split('_')])
        _class = getattr(command, class_name)
        if _class.BinCode.replace('0b', '').zfill(4) == cmd_type:
            args = [reg1, reg2, dest_reg, src]
            return _class(s.REGS, s.MEMORY, args)

    return None


def parse_binary_from_file(filepath: str):
    if not os.path.exists(filepath):
        raise FileExistsError(f'{filepath} not found')

    with open(filepath, 'r', encoding='UTF-8') as f:
        raw = f.read()

        raw = [x for x in raw.replace('\n', '').split(';') if x and not x.startswith('--') and not x.startswith('#')]

        files = os.listdir('source/command')

        python_files = [file for file in files if
                        file.endswith('.py') and not file.startswith('base') and not file.startswith('__')]

        baked_commands = []
        s = Static()
        loops = []
        for i, rc in enumerate(raw):
            # added_in_loop = False
            command = get_command_from_bin(bin(int(rc.strip(), 2))[2:].zfill(32))
            if command is None:
                raise ValueError(f'Can\'t identify the command {rc}')
            # if isinstance(command, BaseWithBodyCommand):
            #     print('LOOP found')
            #     loops.append(command)
            #     continue
            # if len(loops) > 0:
            #     if rc.startswith('    '):
            #         loops[-1].Commands.append(command)
            #         added_in_loop = True
            #     else:
            #         baked_commands.append(loops.pop())
            # if i == len(raw) - 1:
            #     if len(loops) > 0:
            #         for i, loop in enumerate(loops):
            #             if len(loop.Commands) == 0:
            #                 raise RuntimeError('Found LOOP without body')
            #             baked_commands.append(loops[i])
            #         loops.clear()
            # if not added_in_loop:
            baked_commands.append(command)
            # for python_file in python_files:
            #     module_name = python_file[:-3]
            #
            #     command = importlib.import_module(f'source.command.{module_name}')
            #     class_name = ''.join([x.capitalize() for x in module_name.split('_')])
            #     _class = getattr(command, class_name)
            #     if _class.Operation == rc.replace('>', '').strip():
            #         if issubclass(_class, BaseWithBodyCommand):
            #             args = args[0].replace('FROM', '').replace('TO', '').replace('IN', '').strip().split()
            #
            #             loops.append(_class(s.REGS, s.MEMORY, *args))
            #             print(f'Found LOOP')
            #             found = True
            #             break
            #
            #         if len(loops) > 0:
            #             if rc.startswith('>'):
            #                 print(f'Added to LOOP =>  {command.__name__}')
            #                 loops[-1].Commands.append(_class(s.REGS, s.MEMORY, *args))
            #                 found = True
            #             else:
            #                 print(f'LOOP registered')
            #                 baked_commands.append(loops.pop())
            #                 found = True
            #                 break
            #             if i == len(raw) - 1:
            #                 print(f'LOOP registered')
            #                 baked_commands.append(loops.pop())
            #                 found = True
            #             break
            #
            #         # if _class.ArgCount != len(args):
            #         #     raise RuntimeError(
            #         #         f'Invalid args count for {command.__name__}\nWant: {_class.ArgCount}, passed: {len(args)}')
            #         print(f'Found {command.__name__}')
            #         found = True
        #     if not found:
        #         raise RuntimeError(f'{rc} command not found')

        assert len(loops) == 0

        return baked_commands


def parse_text_from_file(filepath: str):
    if not os.path.exists(filepath):
        raise FileExistsError(f'{filepath} not found')

    with open(filepath, 'r', encoding='UTF-8') as f:
        raw = f.read()

        raw = [x.upper() for x in raw.replace('\n', '').split(';') if
               x and not x.startswith('--') and not x.startswith('#')]

        files = os.listdir('source/command')

        python_files = [file for file in files if
                        file.endswith('.py') and not file.startswith('base') and not file.startswith('__')]

        s = Static()
        found_cmds = []
        for i, rc in enumerate(raw):
            found = False
            args = [x.strip() for x in [x.replace(';', '').strip() for x in rc.split(' ', 1)][-1].split(',')]
            rc = rc.split()[0]

            for python_file in python_files:
                module_name = python_file[:-3]

                command = importlib.import_module(f'source.command.{module_name}')
                class_name = ''.join([x.capitalize() for x in module_name.split('_')])
                _class = getattr(command, class_name)
                code = None
                # 0 -> Reg1
                # 1 -> Reg2
                # 2 -> Dst
                # 3 -> Lit
                if _class.Operation == rc.replace('>', '').strip():
                    code = _class.BinCode.replace('0b', '').zfill(4)
                    lit = ''.zfill(16)
                    reg1 = ''.zfill(4)
                    reg2 = ''.zfill(4)
                    dst = ''.zfill(4)
                    # >ADD REG1, 1, REG1;
                    #    0001 0000000000000001 0001 0001 0000;
                    if _class == AddCommand:
                        lit = bin(int(args[1])).zfill(16)
                        reg1 = bin(get_reg_by_name(args[0])).replace('0b', '').zfill(4)
                        dst = bin(get_reg_by_name(args[2])).replace('0b', '').zfill(4)
                    # >LOAD REG1, REG0;
                    #    0101 1000000000000000 0000 0000 0001;
                    elif _class == LoadCommand:
                        if 'REG' in args[0]:
                            lit = '1000000000000000'
                            reg1 = bin(get_reg_by_name(args[0])).replace('0b', '').zfill(4)
                            reg2 = bin(get_reg_by_name(args[0])).replace('0b', '').zfill(4)
                        else:
                            lit = bin(int(args[0])).replace('0b', '').zfill(16)
                        dst = bin(get_reg_by_name(args[1])).replace('0b', '').zfill(4) # 1
                    elif _class == MaxCommand:
                        lit = bin(get_reg_by_name(args[0])).replace('0b', '').zfill(16)
                        reg1 = bin(get_reg_by_name(args[1])).replace('0b', '').zfill(4)
                        dst = bin(get_reg_by_name(args[2])).replace('0b', '').zfill(4)
                    elif _class == SubCommand:
                        dst = bin(get_reg_by_name(args[2])).replace('0b', '').zfill(4)
                        reg1 = bin(get_reg_by_name(args[0])).replace('0b', '').zfill(4)
                        lit = bin(int(args[1])).replace('0b', '').zfill(16)
                    elif _class == JnzCommand:
                        reg1 = bin(get_reg_by_name(args[0])).replace('0b', '').zfill(4)
                        lit = bin(int(args[1])).replace('0b', '').zfill(16)

                    # lit = bin(int(str(lit), 2)).replace('0b', '').zfill(16)
                    # reg1 = bin(int(str(reg1), 2)).replace('0b', '').zfill(4)
                    # reg2 = bin(int(str(reg2), 2)).replace('0b', '').zfill(4)
                    # dst = bin(int(str(dst), 2)).replace('0b', '').zfill(4)

                    found_cmds.append(f'{code}{lit}{dst}{reg1}{reg2}')

        open('tmp', 'w', encoding='UTF-8').write(';\n'.join(found_cmds))

        return parse_binary_from_file('tmp')

# def parse_text_from_file(filepath: str):
#     if not os.path.exists(filepath):
#         raise FileExistsError(f'{filepath} not found')
#
#     with open(filepath, 'r', encoding='UTF-8') as f:
#         raw = f.read()
#
#         raw = [x.upper() for x in raw.replace('\n', '').split(';') if
#                x and not x.startswith('--') and not x.startswith('#')]
#
#         files = os.listdir('source/command')
#
#         python_files = [file for file in files if
#                         file.endswith('.py') and not file.startswith('base') and not file.startswith('__')]
#
#         baked_commands = []
#         s = Static()
#         loops = []
#         for i, rc in enumerate(raw):
#             found = False
#             args = [x.strip() for x in [x.replace(';', '').strip() for x in rc.split(' ', 1)][-1].split(',')]
#             rc = rc.split()[0]
#             for python_file in python_files:
#                 module_name = python_file[:-3]
#
#                 command = importlib.import_module(f'source.command.{module_name}')
#                 class_name = ''.join([x.capitalize() for x in module_name.split('_')])
#                 _class = getattr(command, class_name)
#                 if _class.Operation == rc.replace('>', '').strip():
#                     if issubclass(_class, BaseWithBodyCommand):
#                         args = args[0].replace('FROM', '').replace('TO', '').replace('IN', '').strip().split()
#
#                         loops.append(_class(s.REGS, s.MEMORY, args))
#                         print(f'Found LOOP')
#                         found = True
#                         break
#
#                     if len(loops) > 0:
#                         if rc.startswith('>'):
#                             print(f'Added to LOOP =>  {command.__name__}')
#                             loops[-1].Commands.append(_class(s.REGS, s.MEMORY, args))
#                             found = True
#                         else:
#                             print(f'LOOP registered')
#                             baked_commands.append(loops.pop())
#                             found = True
#                             break
#                         if i == len(raw) - 1:
#                             print(f'LOOP registered')
#                             baked_commands.append(loops.pop())
#                             found = True
#                         break
#
#                     # if _class.ArgCount != len(args):
#                     #     raise RuntimeError(
#                     #         f'Invalid args count for {command.__name__}\nWant: {_class.ArgCount}, passed: {len(args)}')
#                     print(f'Found {command.__name__}')
#                     found = True
#                     baked_commands.append(_class(s.REGS, s.MEMORY, args))
#             if not found:
#                 raise RuntimeError(f'{rc} command not found')
#
#         assert len(loops) == 0
#
#         return baked_commands
