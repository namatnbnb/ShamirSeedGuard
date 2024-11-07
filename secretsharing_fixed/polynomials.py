import random

def extended_gcd(a, b):
    """
    Division in integers modulus p means finding the inverse of the
    denominator modulo p and then multiplying the numerator by this
    inverse (Note: inverse of A is B such that A*B % p == 1).
    This can be computed via the extended Euclidean algorithm:
    http://en.wikipedia.org/wiki/Modular_multiplicative_inverse#Computation
    """
    x = 0
    last_x = 1
    y = 1
    last_y = 0
    while b != 0:
        quot = a // b
        a, b = b, a % b
        x, last_x = last_x - quot * x, x
        y, last_y = last_y - quot * y, y
    return last_x

def div_mod(num, den, p):
    """ Compute num / den modulo prime p
    To explain this, the result will be such that: 
    den * result = num (mod p)
    """
    inv = extended_gcd(den, p)
    return num * inv

def random_polynomial(degree, intercept, upper_bound):
    """ Generates a random polynomial with positive coefficients.
    """
    if degree < 0:
        raise ValueError('Degree must be a non-negative number.')
    coefficients = [intercept]
    for i in range(degree):
        coefficients.append(random.randint(0, upper_bound-1))
    return coefficients

def get_polynomial_points(coefficients, num_points, prime):
    """ Calculates the first n points of a polynomial with given coefficients.
    """
    points = []
    for x in range(1, num_points+1):
        # start with x=1 and calculate the value of y
        y = coefficients[0]
        # calculate each term and add it to y, using modular math
        for i in range(1, len(coefficients)):
            exponentiation = (x**i) % prime
            term = (coefficients[i] * exponentiation) % prime
            y = (y + term) % prime
        # add the point to the list of points
        points.append((x, y))
    return points

def modular_lagrange_interpolation(x, points, prime):
    """
    Find the y-value for the given x, given n (x, y) points;
    k points will define a polynomial of up to kth order.
    """
    k = len(points)
    if k < 2:
        raise ValueError("Need at least 2 points for interpolation")
    nums = []  # avoid inexact division
    dens = []
    for i in range(k):
        others = list(points)
        cur = others.pop(i)
        nums.append(1)
        dens.append(1)
        for j in range(len(others)):
            cur_x = cur[0]
            other_x = others[j][0]
            nums[i] = (nums[i] * (x - other_x)) % prime
            dens[i] = (dens[i] * (cur_x - other_x)) % prime
    den = 1
    for i in range(k):
        den = (den * dens[i]) % prime
    num = 0
    for i in range(k):
        num_i = (nums[i] * points[i][1] * 
                div_mod(den, dens[i], prime)) % prime
        num = (num + num_i) % prime
    return (num * div_mod(1, den, prime)) % prime
