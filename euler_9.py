import math

def main():
    #average run-time: 45.0ms
    for a in range (1, 1000):
        for b in range (1, a):
            if math.sqrt(a**2 + b**2) - math.floor((math.sqrt(a**2 + b**2))) == 0:
                if a + b + math.sqrt(a**2 + b**2) == 1000:
                    return a * b * int(math.sqrt(a**2 + b**2))

if __name__ == '__main__':
    main()
