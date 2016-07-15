def main():
    fibs = [1,2]
    even_sum = fibs[1]
    breaker = False
    while breaker == False:
        for n in range(3):
            fibs.append(fibs[-1] + fibs[-2])

        if fibs[-1] <= 4e30:
            print fibs[-1]
            even_sum += fibs[-1]
        else:
            breaker = True
            print breaker

        del fibs[0:3]
    print even_sum
    print fibs


if __name__ == '__main__':
    main()
