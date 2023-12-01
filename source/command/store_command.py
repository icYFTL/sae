from .base_command import BaseCommand
from ..enums import CommandType
from ..utils import get_reg_by_code


class StoreCommand(BaseCommand):
    Operation = 'STORE'
    ArgCount = 4
    BinCode = bin(9)
    BinType = CommandType.Basic

    def __init__(self, regs, memory, args):
        super().__init__(regs, memory, args)

    def run(self):
        if not self._args[2].IsReg:
            raise RuntimeError(f'Last arg of {self.__class__.__name__} must be REGX')

        reg_ix = get_reg_by_code(self._args[1].Value)
        mem_ix = int(self._args[3].Value)

        self._memory[mem_ix] = self._regs[reg_ix]
