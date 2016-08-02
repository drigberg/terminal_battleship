def main():
    l1 = []
    N = 102
    n = -1
    while n < N:
      n += 2
      l1.append(n)
    l1.pop(0)
    print l1
    for i in l1:

      for x in l1:

          if i % x == 0 and i != x:

              l1.remove(i)
              break
    print l1
    len(l1)

if __name__ == '__main__':
    main()
