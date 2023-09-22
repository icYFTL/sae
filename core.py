from random import randint


class Static(object):
    REGS = [0, 0, 0]
    MEMORY = [randint(0, 100) for _ in range(15)]  # Гарвардка, поэтому память хранится отдельно от команд

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Static, cls).__new__(cls)
        return cls.instance
