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


def main():
    base_dir = Path(__file__).cwd()
    data = base_dir.joinpath("data")
    new_data = data.joinpath("name")
    new_data.mkdir()

    for child in data.iterdir():
        print(type(child))

if __name__ == "__main__":
    main()