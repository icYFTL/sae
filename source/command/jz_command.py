from .base_logic_command import BaseLogicCommand
from ..enums import CommandType
from ..utils import get_reg_by_code


class JzCommand(BaseLogicCommand):
    Operation = 'JZ'
    ArgCount = 4
    BinCode = bin(4)
    BinType = CommandType.Logical

    def __init__(self, regs, memory, args):
        super().__init__(regs, memory, args)

    def run(self):
        return self._regs[get_reg_by_code(self._args[0].Value)] != 0, self._args[3].Value
