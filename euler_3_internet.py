def main():
    n = 600851475143
    i = 2
    while i * i < n:
         while n % i == 0:
             n = n / i
         i = i + 1

    return n

if __name__ == '__main__':
    main()
