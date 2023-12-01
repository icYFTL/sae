from enum import Enum


class CommandType(Enum):
    Basic = bin(1),
    WithBody = bin(2),
    Logical = bin(3)
