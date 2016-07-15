import math

def main():
    num = 600851475143
    factors= []
    for a in range(1, int(math.sqrt(num))):
        if num % a == 0:
            factors.append(a)

    for n in range(len(factors)):
        if factors[n] != None:
            for b in range (2, int(math.sqrt(factors[n]))):
                if factors[n] % b == 0:
                    factors[n] = None
                    break
                continue
    return max(factors)

if __name__ == '__main__':
    main()
