from .base_command import BaseCommand
from ..utils import get_reg


class StoreCommand(BaseCommand):
    Operation = 'STORE'
    ArgCount = 2

    def __init__(self, regs, memory, *args):
        super().__init__(regs, memory, args)

    def run(self):
        if self._args[-1].IsReg:
            raise RuntimeError(f'Last arg of {self.__class__.__name__} must be index of memory array')
        
        if self._args[0].IsReg:
            result = self._regs[get_reg(self._args[0].Value)]
        else:
            result = int(self._args[0].Value)

        self._memory[int(self._args[-1].Value)] = result
