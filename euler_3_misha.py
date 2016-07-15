import math
def main():
    num = 600851475143
    list_primes= []
    a = 0
    while a < num:
        a += 1
        if num % a == 0:
            list_primes.append(a)
        if a % 100000 == 0:
            print a

    trash = []
    primes = []

    for pos_prime in list_primes:
        b = 1
        while b < pos_prime:
            b += 1
            if pos_prime % b == 0 and b != pos_prime:
                trash.append(pos_prime)
                break
            continue
    for t in trash:
        list_primes.remove(t)
    print list_primes[-1]

if __name__ == '__main__':
    main()
