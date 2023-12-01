from .base_command import BaseCommand

class BaseLogicCommand(BaseCommand):
    def __init__(self, regs, memory, args):
        super().__init__(regs, memory, args)

    def run(self):
        raise NotImplemented()