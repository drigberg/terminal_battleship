import math

def main():
    n = 0
    while n is not None:
        n = n + 2520
        for a in range(11, 20):
            if n % a != 0:
                break
        else:
            return n
            n = None

if __name__ == '__main__':
    main()
