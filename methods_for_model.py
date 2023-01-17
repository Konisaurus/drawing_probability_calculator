def faculty(n):
    # calculate faculty of n and return it.
    n_fak = 1
    if n != 0:
        for i in range(2,n+1):
            n_fak *= i
    return n_fak


def binomial_coefficient(n, k):
    # calculates the binomial coefficient and return it.
    # n = set
    # k = draws
    if 0 <= k <= n:
        dividend = 1
        divisor = 1
        for i in range(1, min(n - k, k) + 1):
            dividend *= n
            divisor *= i
            n -= 1
        return int(dividend / divisor)


def format_float(percentage, decimals, value):
    # formating method for floats, returns the newly formated float.
    # percentage: True = multiply float by 100, False = do nothing
    # decimals: number of decimals after the comma
    # value: float you want to format
    if percentage == True:
        value *= 100
    return float("%.{}f".format(decimals) % value)
    