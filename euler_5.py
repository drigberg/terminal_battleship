import math

def main():
    #could be faster by incrementing by 2520 (10*9*8...*1), but this is
    #coded for versatility, not optimum usage of all given info
    n = 0
    while n is not None:
        n = n + 20
        for a in range(11, 20):
            if n % a != 0:
                break
        else:
            return n
            n = None

if __name__ == '__main__':
    main()
