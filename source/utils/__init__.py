def get_reg_by_name(name):
    if name == 'REG0':
        return 0
    elif name == 'REG1':
        return 1
    elif name == 'REG2':
        return 2
    elif name == 'REG3':
        return 3

    raise ValueError(f'Register {name} not found')

def get_reg_by_code(code):
    code = str(code)
    if code == '0000' or code == '0':
        return 0
    elif code == '0001' or code == '1':
        return 1
    elif code == '0010' or code == '2':
        return 2
    elif code == '0011' or code == '3':
        return 3

    raise ValueError(f'Register with code {str(code)} not found')