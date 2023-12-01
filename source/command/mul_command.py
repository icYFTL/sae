from .base_command import BaseCommand
from ..enums import CommandType
from ..utils import get_reg_by_name


class MulCommand(BaseCommand):
    Operation = 'MUL'
    ArgCount = 4
    BinCode = bin(8)
    BinType = CommandType.Basic

    def __init__(self, regs, memory, args):
        super().__init__(regs, memory, args)

    def run(self):
        if not self._args[2].IsReg:
            raise RuntimeError(f'Last arg of {self.__class__.__name__} must be REGX')

        result = 1
        for arg in self._args:
            if arg.IsReg:
                result *= self._regs[get_reg_by_name(arg.Value)]
            else:
                result *= int(arg.Value)

        reg_ix = get_reg_by_name(self._args[2].Value)
        self._regs[reg_ix] = result
