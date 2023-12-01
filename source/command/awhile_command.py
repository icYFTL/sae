from .base_withbody_command import BaseWithBodyCommand
from source.utils import get_reg_by_code
from ..enums import CommandType


class AwhileCommand(BaseWithBodyCommand):
    Operation = 'AWHILE'
    ArgCount = 4
    BinCode = bin(11)
    BinType = CommandType.Basic

    def __init__(self, regs, memory, args):
        super().__init__(regs, memory, args)

    def run(self):
        self.name = self._args[3]
        into = self._memory[0]
        print(f'Into => {into}')
        if len(self._memory) == 0:
            return False

        self._memory[0] -= 1
        return True

        # for cmd in self.Commands:
        #     print(f'Inloop call -> {cmd}')
        #     cmd.run()
