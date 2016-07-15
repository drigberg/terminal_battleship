import datetime
import sys
import euler_5 as timed_script
import euler_5_misha as timed_script2


def main():
    elapsed_list = []
    for n in range(int(sys.argv[1])):
        starttime = datetime.datetime.now()
        output = timed_script.main()
        endtime = datetime.datetime.now()
        elapsed = (endtime - starttime).total_seconds()
        elapsed_list.append(elapsed)
        avg_elapsed = sum(elapsed_list) / len(elapsed_list) * 1000
    print "Dan's script took average time of %s ms to find value of %s" % (avg_elapsed, output)

    elapsed_list = []
    for n in range(int(sys.argv[1])):
        starttime = (datetime.datetime.now())
        output = timed_script2.main()
        endtime = datetime.datetime.now()
        elapsed = (endtime - starttime).total_seconds()
        elapsed_list.append(elapsed)
        avg_elapsed = sum(elapsed_list) / len(elapsed_list) * 1000

    print "Misha's script took average time of %s ms to find value of %s" % (avg_elapsed, output)


if __name__ == '__main__':
    main()
