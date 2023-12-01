from .base_command import BaseCommand


class BaseWithBodyCommand(BaseCommand):
    Commands = []

    def __init__(self, regs, memory, args):
        self.name = None
        super().__init__(regs, memory, args)

    def run(self):
        raise NotImplemented()

    def run_next(self, next_routine):
        raise NotImplemented()
