
def is_number(s):
    if s:
        if s[0] == '-':
            s = s[1:]
    else:
        return False
    if s:
        for i in s:
            if i < '0' or i > '9':
                return False
        return True
    return False
