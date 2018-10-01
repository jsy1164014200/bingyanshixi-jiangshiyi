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

def order_by_id(item):
    return item["id"]

def main():
    # base_dir = Path(__file__).cwd()
    # data = base_dir.joinpath("data")
    # table = data.joinpath("hahah","test1.csv")
    # with open(table,"r",newline="") as csvfile:
    #     reader = csv.DictReader(csvfile,delimiter="|")
    #     for row in reader:
    #         print(row)
    l = [{"id":1,"name":"jsy"},{"id":10,"name":"haha"},{"id":3,"name":"asd"}]
    l.sort(key=order_by_id)
    print(l)
if __name__ == "__main__":
    main()