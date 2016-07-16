import math
def main():
    n = 1
    primes_count = 0
    while n:
        n += 1
        for a in range(2, int(math.floor(math.sqrt(n))) + 1):
            if n % a == 0:
                break
        else:
            primes_count += 1
            print primes_count

        if primes_count == 10001:
            break

    return n

if __name__ == '__main__':
    main()
