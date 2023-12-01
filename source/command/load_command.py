from .base_command import BaseCommand
from ..enums import CommandType
from ..utils import get_reg_by_code


class LoadCommand(BaseCommand):
    Operation = 'LOAD'
    ArgCount = 4
    BinCode = bin(5)
    BinType = CommandType.Basic

    def __init__(self, regs, memory, args):
        super().__init__(regs, memory, args)

    def run(self):
        if not self._args[2].IsReg:
            raise RuntimeError(f'Last arg of {self.__class__.__name__} must be REGX')

        reg_ix = get_reg_by_code(self._args[2].Value)
        mem_ix = int(self._args[3].Value)
        if mem_ix == 32768:  # Magic
            mem_ix = self._regs[get_reg_by_code(self._args[1].Value)]

        self._regs[reg_ix] = self._memory[mem_ix]

        # spc_val = None
        # if self._args[0].IsReg:
        #     rix = get_reg_by_name(self._args[0].Value)
        #     spc_val = self._regs[rix]
        #     self._regs[reg_ix] = self._memory[spc_val]
        # else:
        #     self._regs[reg_ix] = self._memory[int(self._args[0].Value)]
