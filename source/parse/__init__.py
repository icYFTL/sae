import os
import importlib
import re

from core import Static


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


def parse_from_file(filepath: str):
    if not os.path.exists(filepath):
        raise FileExistsError(f'{filepath} not found')

    with open(filepath, 'r', encoding='UTF-8') as f:
        raw = f.read()

        raw = [x.strip().upper() for x in raw.replace('\n', '').split(';') if x and not x.startswith('--')]

        files = os.listdir('source/command')

        python_files = [file for file in files if
                        file.endswith('.py') and not file.startswith('base') and not file.startswith('__')]

        baked_commands = []
        s = Static()
        for rc in raw:
            found = False
            args = [x.strip() for x in [x.replace(';', '').strip() for x in rc.split(' ', 1)][-1].split(',')]
            rc = rc.split()[0]
            for python_file in python_files:
                module_name = python_file[:-3]

                command = importlib.import_module(f'source.command.{module_name}')
                class_name = ''.join([x.capitalize() for x in module_name.split('_')])
                _class = getattr(command, class_name)
                if _class.Operation == rc:
                    # if _class.ArgCount != len(args):
                    #     raise RuntimeError(
                    #         f'Invalid args count for {command.__name__}\nWant: {_class.ArgCount}, passed: {len(args)}')
                    print(f'Found {command.__name__}')
                    found = True
                    baked_commands.append(_class(s.REGS, s.MEMORY, *args))
            if not found:
                raise RuntimeError(f'{rc} command not found')

        return baked_commands
