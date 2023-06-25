def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def calculate_pi_leibniz(n):
    pi = 0
    sign = 1
    denominator = 1
    for _ in range(n):
        term = sign / denominator
        pi += term
        sign *= -1
        denominator += 2
    pi *= 4
    return pi


def calculate_sum(numbers):
    return sum(numbers)


def add(a, b):
    return a + b
