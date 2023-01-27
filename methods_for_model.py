'''
Contains some basic methods for the model.

Included are:
- faculty()
- biomial_coefficient()
- format_float()
'''

# Methods.
def faculty(n):
    '''
    Calculates the faculty n! and returns it.
    '''
    if n < 0 or type(n) != int:
        raise TypeError("not a positive integer.")
    
    n_fak = 1                   # The smallest possible result of faculty is 1.
    if n != 0:                  # 0! is defined as 1.
        for i in range(2,n+1):  # Increase i by one and multiply it with the result before, until i reaches n.
            n_fak *= i
            
    return n_fak                # return result = n!


def binomial_coefficient(n, k):
    '''
    Calculates the binomial coefficient.

    It is defined as:
    n! / [k! * (n - k)!]

    n: The total of distinct items.
    k: Number of particular items chosen from the total.
    
    Note that n >= k >= 0.

    Because faculties have a lot of same factors, we do not have calculate
    the complete faculties. The following code is a more effiecient implementation
    of the binomial coefficient.
    '''
    if 0 <= k <= n:                             
        dividend = 1
        divisor = 1
        for i in range(1, min(n - k, k) + 1):
            dividend *= n
            divisor *= i
            n -= 1
        return int(dividend / divisor)
    
    else:
        raise ("only positive integers which fulfil n >= k >= 0.")


def format_float(percentage, decimals, value):
    '''
    Formats a float and returns it as a float
    Percentage: True = multiply the float by 100, False = do nothing.
    Decimals: Number of decimals after the coma.
    Value: Flota you want to format.
    '''
    if percentage == True:
        value *= 100

    return float("%.{}f".format(decimals) % value)
