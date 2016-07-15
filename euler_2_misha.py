def main():
    l = [1,2]
    while l[-1] < 4e99:
        z = l[-1]+l[-2]
        l.append(z)
    al = l[0:-1]
    sas = []
    for x in al:
        if x % 2 == 0:
            sas.append(x)
    even_sum = sum(sas)
    return even_sum

if __name__ == '__main__':
    main()
