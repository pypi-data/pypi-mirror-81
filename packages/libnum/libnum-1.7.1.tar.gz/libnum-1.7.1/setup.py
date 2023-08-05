# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['libnum']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'libnum',
    'version': '1.7.1',
    'description': 'Working with numbers (primes, modular, etc.)',
    'long_description': "# libnum\n\nThis is a python library for some numbers functions:\n\n*  working with primes (generating, primality tests)\n*  common maths (gcd, lcm, n'th root)\n*  modular arithmetics (inverse, Jacobi symbol, square root, solve CRT)\n*  converting strings to numbers or binary strings\n\nLibrary may be used for learning/experimenting/research purposes. Should NOT be used for secure crypto implementations.\n\n## Installation\n\n```bash\n$ pip install libnum\n```\n\nNote that only Python 3 version is maintained.\n\n## Development\n\nFor development or building this repository, [poetry](https://python-poetry.org/) is needed.\n\nTests can be ran with\n\n```bash\n$ pytest --doctest-modules .\n```\n\n## List of functions\n\n<b>Common maths</b>\n\n*  len\\_in\\_bits(n) - number of bits in binary representation of @n\n*  randint\\_bits(size) - random number with a given bit size\n*  extract\\_prime\\_power(a, p) - s,t such that a = p**s * t\n*  nroot(x, n) - truncated n'th root of x\n*  gcd(a, b, ...) - greatest common divisor of all arguments\n*  lcm(a, b, ...) - least common multiplier of all arguments\n*  xgcd(a, b) - Extented Euclid GCD algorithm, returns (x, y, g) : a * x + b * y = gcd(a, b) = g\n\n<b>Modular</b>\n\n*  has\\_invmod(a, n) - checks if a has modulo inverse\n*  invmod(a, n) - modulo inverse\n*  solve\\_crt(remainders, modules) - solve Chinese Remainder Theoreme\n*  factorial\\_mod(n, factors) - compute factorial modulo composite number, needs factorization\n*  nCk\\_mod(n, k, factors) - compute combinations number modulo composite number, needs factorization\n*  nCk\\_mod\\_prime\\_power(n, k, p, e) - compute combinations number modulo prime power\n\n<b>Modular square roots</b>\n\n*  jacobi(a, b) - Jacobi symbol\n*  has\\_sqrtmod\\_prime\\_power(a, p, k) - checks if a number has modular square root, modulus is p**k\n*  sqrtmod\\_prime\\_power(a, p, k) - modular square root by p**k\n*  has\\_sqrtmod(a, factors) - checks if a composite number has modular square root, needs factorization\n*  sqrtmod(a, factors) - modular square root by a composite modulus, needs factorization\n\n<b>Primes</b>\n\n*  primes(n) - list of primes not greater than @n, slow method\n*  generate\\_prime(size, k=25) - generates a pseudo-prime with @size bits length. @k is a number of tests.\n*  generate\\_prime\\_from\\_string(s, size=None, k=25) - generate a pseudo-prime starting with @s in string representation\n\n<b>Factorization</b>\n*  is\\_power(n) - check if @n is p**k, k >= 2: return (p, k) or False\n*  factorize(n) - factorize @n (currently with rho-Pollard method)\nwarning: format of factorization is now dict like {p1: e1, p2: e2, ...}\n\n<b>ECC</b>\n\n*  Curve(a, b, p, g, order, cofactor, seed) - class for representing elliptic curve. Methods:\n*   .is\\_null(p) - checks if point is null\n*   .is\\_opposite(p1, p2) - checks if 2 points are opposite\n*   .check(p) - checks if point is on the curve\n*   .check\\_x(x) - checks if there are points with given x on the curve (and returns them if any)\n*   .find\\_points\\_in\\_range(start, end) - list of points in range of x coordinate\n*   .find\\_points\\_rand(count) - list of count random points\n*   .add(p1, p2) - p1 + p2 on elliptic curve\n*   .power(p, n) - n✕P or (P + P + ... + P) n times\n*   .generate(n) - n✕G\n*   .get\\_order(p, limit) - slow method, trying to determine order of p; limit is max order to try\n\n<b>Converting</b>\n\n*  s2n(s) - packed string to number\n*  n2s(n) - number to packed string\n*  s2b(s) - packed string to binary string\n*  b2s(b) - binary string to packed string\n\n<b>Stuff</b>\n\n*  grey\\_code(n) - number in Grey code\n*  rev\\_grey\\_code(g) - number from Grey code\n*  nCk(n, k) - number of combinations\n*  factorial(n) - factorial\n\n## About\n\nAuthor: hellman\n\nLicense: [MIT License](http://opensource.org/licenses/MIT)\n",
    'author': 'hellman',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
