from .base_command import BaseCommand
from ..enums import CommandType
from ..utils import get_reg_by_name
from math import inf


class DivCommand(BaseCommand):
    Operation = 'DIV'
    ArgCount = 4
    BinCode = bin(3)
    BinType = CommandType.Basic

    def __init__(self, regs, memory, args):
        super().__init__(regs, memory, args)

    def run(self):
        if not self._args[2].IsReg:
            raise RuntimeError(f'Last arg of {self.__class__.__name__} must be REGX')

        result = []
        for arg in self._args:
            if arg.IsReg:
                result.append(self._regs[get_reg_by_name(arg.Value)])
            else:
                result.append(int(arg.Value))

        reg_ix = get_reg_by_name(self._args[2].Value)
        if result[1] == 0:
            self._regs[reg_ix] = inf  # Let's have some fun
            return

        self._regs[reg_ix] = result[0] / result[1]
