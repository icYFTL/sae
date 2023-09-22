def get_reg(name):
    if name == 'REG0':
        return 0
    elif name == 'REG1':
        return 1
    elif name == 'REG2':
        return 2

    raise ValueError(f'Register {name} not found')
