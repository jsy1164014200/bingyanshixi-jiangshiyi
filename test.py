    # with open("eggs.csv","w",newline="") as csvfile:
    #     writer = csv.writer(csvfile,delimiter="|",quoting=csv.QUOTE_MINIMAL)
    #     writer.writerow(["span","dkfj","fkdj","kdfjksdj","fdjk"])
    #     writer.writerow(["sapn","Lovely spam","wonderful Spam"])
    #     writer.writerow(["haha",None,"dkfj",None,"jiangshiyi",None])

    # with open("eggs.csv","r",newline="") as csvfile:
    #     reader = csv.DictReader(csvfile,delimiter="|")
    #     for row in reader:
    #         print(row["dkfj"])
from pathlib import Path
import csv
import cross_platform_lock
import threading
import time
import sys
from io import StringIO


def main():
    # base_dir = Path(__file__).cwd()
    # data = base_dir.joinpath("data")
    # table = data.joinpath("hahah","test1.csv")
    # with open(table,"r",newline="") as csvfile:
    #     reader = csv.DictReader(csvfile,delimiter="|")
    #     for row in reader:
    #         print(row)
    base_dir = Path(__file__).cwd()
    log = base_dir.joinpath("log.txt")

    # id = threading.currentThread().getName()
    # with open(log,"a") as fp :
    #     cross_platform_lock.lock(fp,cross_platform_lock.LOCK_EX) # 加锁
    #     print("{0} acquire lock.".format(id))
    #     fp.write("dslkf\n")
    #     time.sleep(3)
    #     print("LOCK release?")

    # with open(log,"a") as fp:
    #     cross_platform_lock.lock(fp,cross_platform_lock.LOCK_EX)
    #     fp.write("dkfjksdjfksdjk\n")
    #     time.sleep(3)
    # fp = open(log,"a") 
    # cross_platform_lock.lock(fp,cross_platform_lock.LOCK_EX)
    # print("{0} acquire lock.".format(id))
    # fp.write("{0} ksdfjk\n".format(id))
    # time.sleep(3)
    # fp.write("{0} ksdfjk\n".format(id))


    # print("{0} exit.".format(id))
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    print("lkdsfjklsj")
    s = sys.stdout.getvalue()

    sys.stdout = old_stdout
    print(s)






if __name__ == "__main__":
    # for i in range(5):
    #     myThread = threading.Thread(target=main)
    #     myThread.start()
    main()