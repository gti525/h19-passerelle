from random import randint


def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)



def add_leading_zero(text):
    if len(str(text)) == 2:
        return str(text)
    elif len(str(text)) == 1:
        return "0{}".format(str(text))
    else:
        return text
