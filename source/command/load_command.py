from .base_command import BaseCommand
from ..utils import get_reg


class LoadCommand(BaseCommand):
    Operation = 'LOAD'
    ArgCount = 2

    def __init__(self, regs, memory, *args):
        super().__init__(regs, memory, args)

    def run(self):
        if not self._args[1].IsReg:
            raise RuntimeError(f'Last arg of {self.__class__.__name__} must be REGX')

        reg_ix = get_reg(self._args[1].Value)
        self._regs[reg_ix] = self._memory[int(self._args[0].Value)]
