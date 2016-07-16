def main():
  a = 0
  check = 10
  while check > 0:
      check += 1
      i = 1

      while i < 20:
          i += 1
          if check % i == 0:
              if i == 20:
                  a += check
                  return check
          else:
              break
      if a != 0:
          break

if __name__ == '__main__':
    main()
