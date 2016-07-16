def main():
    #run-time: 0.004ms
    fibs = [1,2]
    even_sum = fibs[1]
    while fibs:
        fibs.append(fibs[-1] + fibs[-2])
        if fibs[-1] % 2 == 0:
            even_sum += fibs[-1]
        else:
            break

    return even_sum

if __name__ == '__main__':
    main()
