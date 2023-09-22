from dataclasses import dataclass
from typing import Any
import re
import ast

from ..utils import get_reg


@dataclass()
class ArgContainer:
    Value: Any
    IsReg: bool = False

    def __str__(self):
        return str(self.Value)


class BaseCommand:
    Operation = None
    ArgCount = -1

    def __init__(self, regs, memory, *args):
        self._regs = regs
        self._memory = memory
        self._args = [x.strip() for x in args[0]]
        self._args_setup()

    def __str__(self):
        return f'{self.Operation} {" ".join([str(x) for x in self._args])}'

    def run(self):
        raise NotImplemented()

    def _args_setup(self):
        reg_rx = re.compile(r'^REG\d{1,}$')

        if self.ArgCount != len(self._args):
            raise RuntimeError(f'ArgsSettings bad configuration for {self.__class__.__name__}')

        backed_args = []

        for i, arg in enumerate(self._args):
            # if self.ArgsSettings[i].IsReg:
            if reg_rx.match(arg):
                try:
                    get_reg(arg)
                    backed_args.append(ArgContainer(arg, True))
                    continue
                except:
                    raise RuntimeError(f'Invalid reg passed {arg} in {self.__class__.__name__}')
                # if type(arg) != self.ArgsSettings[i].Type:
                #     try:
                #         arg = ast.literal_eval(arg)
                #     except (ValueError, SyntaxError):
                #         raise TypeError(
                #             f'Can\'t cast {arg} from {type(arg)} to target {self.ArgsSettings[i].Type} in {self.__class__.__name__}')
                #
                #     if type(arg) != self.ArgsSettings[i].Type:
                #         raise TypeError(f'Bad arg type for argument {arg} in {self.__class__.__name__}')
            try:
                arg = ast.literal_eval(arg)
            except (ValueError, SyntaxError):
                raise TypeError(
                    f'Can\'t cast {arg} from {type(arg)} to target int in {self.__class__.__name__}')

            backed_args.append(ArgContainer(arg, False))

        self._args = backed_args
