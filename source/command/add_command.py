from .base_command import BaseCommand
from ..utils import get_reg_by_code
from ..enums import CommandType


class AddCommand(BaseCommand):
    Operation = 'ADD'
    ArgCount = 4
    BinCode = bin(1)
    BinType = CommandType.Basic

    def __init__(self, regs, memory, args):
        super().__init__(regs, memory, args)

    def run(self):
        if not self._args[2].IsReg:
            raise RuntimeError(f'Last arg of {self.__class__.__name__} must be REGX')

        # result = 0
        # for arg in self._args[:2]:
        #     if arg.IsReg:
        #         result += self._regs[get_reg_by_code(arg.Value)]
        #     else:
        #         result += int(arg.Value)

        reg_ix = get_reg_by_code(self._args[2].Value)
        self._regs[reg_ix] = self._regs[get_reg_by_code(self._args[0].Value)] + self._args[3].Value
