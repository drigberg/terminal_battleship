def main():
    #all code to be run goes here, in the main function
    #to run: type "python [filename]" while in that file's directory
    list = []
    x = 2
    while x < 100:
        print x
        x = x + 3
        list.append(x)

    print "There are %s items in this list, and the highest value is %s" % (len(list), max(list))























#this tells python to actually run the main function
if __name__ == '__main__':
    main()
