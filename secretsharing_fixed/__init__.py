import random
from .charset import charset_to_int, int_to_charset, base58_chars, base32_chars, zbase32_chars
from .primes import get_large_enough_prime
from .polynomials import random_polynomial, get_polynomial_points, modular_lagrange_interpolation

__version__ = '0.2.6'

def split_secret(secret, share_threshold, num_shares):
    if share_threshold > num_shares:
        raise ValueError("Threshold cannot be greater than the total number of shares")

    if isinstance(secret, str):
        secret_int = charset_to_int(secret, base58_chars)
        if secret != int_to_charset(secret_int, base58_chars):
            raise ValueError('The secret must only contain characters in the supported character set.')
    else:
        secret_int = secret

    prime = get_large_enough_prime([secret_int])

    coefficients = random_polynomial(share_threshold-1, secret_int, prime)
    points = get_polynomial_points(coefficients, num_shares, prime)

    shares = []
    for point in points:
        share = point[1]
        shares.append(share)

    return shares

def recover_secret(shares):
    shares = list(set(shares))  # Remove duplicates
    if len(shares) < 2:
        raise ValueError("Need at least 2 shares")

    points = [(i+1, share) for i, share in enumerate(shares)]
    prime = get_large_enough_prime(shares)
    
    secret_int = modular_lagrange_interpolation(0, points, prime)
    secret = int_to_charset(secret_int, base58_chars)
    
    return secret

class SecretSharer(object):
    """Simple wrapper around split_secret and recover_secret."""
    
    @staticmethod
    def split_secret(secret_string, share_threshold, num_shares):
        shares = split_secret(secret_string, share_threshold, num_shares)
        return shares

    @staticmethod
    def recover_secret(shares):
        secret = recover_secret(shares)
        return secret
