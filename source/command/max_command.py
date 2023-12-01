from .base_command import BaseCommand
from ..enums import CommandType
from ..utils import get_reg_by_code


class MaxCommand(BaseCommand):
    Operation = 'MAX'
    ArgCount = 4
    BinCode = bin(7)
    BinType = CommandType.Basic

    def __init__(self, regs, memory, args):
        super().__init__(regs, memory, args)

    def run(self):
        if not self._args[2].IsReg:
            raise RuntimeError(f'Last arg of {self.__class__.__name__} must be REGX')

        result = []
        for arg in self._args:
            if arg.IsReg:
                result.append(self._regs[get_reg_by_code(arg.Value)])
            else:
                result.append(int(arg.Value))

        result = max(result)

        reg_ix = get_reg_by_code(self._args[2].Value)
        self._regs[reg_ix] = result
