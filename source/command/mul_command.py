from .base_command import BaseCommand
from ..utils import get_reg


class MulCommand(BaseCommand):
    Operation = 'MUL'
    ArgCount = 3

    def __init__(self, regs, memory, *args):
        super().__init__(regs, memory, args)

    def run(self):
        if not self._args[2].IsReg:
            raise RuntimeError(f'Last arg of {self.__class__.__name__} must be REGX')

        result = 1
        for arg in self._args:
            if arg.IsReg:
                result *= self._regs[get_reg(arg.Value)]
            else:
                result *= int(arg.Value)

        reg_ix = get_reg(self._args[2].Value)
        self._regs[reg_ix] = result
