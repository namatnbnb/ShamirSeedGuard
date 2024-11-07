import string

def int_to_charset(val, charset):
    """ Turn a non-negative integer into a string.
    """
    if val < 0:
        raise ValueError('Only non-negative integers are supported.')
    if val == 0:
        return charset[0]
    output = ''
    while val > 0:
        val, digit = divmod(val, len(charset))
        output += charset[digit]
    # reverse the characters in the output and return
    return output[::-1]

def charset_to_int(s, charset):
    """ Turn a string into a non-negative integer.
    """
    output = 0
    for char in s:
        output = output * len(charset) + charset.index(char)
    return output

# base58 characters
base58_chars = string.digits + string.ascii_uppercase + string.ascii_lowercase
base58_chars = base58_chars.replace('0', '').replace('O', '').replace('I', '').replace('l', '')

# base32 characters
base32_chars = string.digits + string.ascii_uppercase
base32_chars = base32_chars.replace('0', '').replace('O', '').replace('I', '').replace('L', '')

zbase32_chars = "ybndrfg8ejkmcpqxot1uwisza345h769"
