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
    with open(log,"a") as fp :
        fp.write("dslkf\n")
        fp.write("Dfkjk\n")
        fp.write("Dfkjk\n")



if __name__ == "__main__":
    main()