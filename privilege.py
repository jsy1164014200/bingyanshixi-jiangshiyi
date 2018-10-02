from pathlib import Path
import csv

base_dir = Path(__file__).cwd()
userfile = base_dir.joinpath("user.csv")




def handle(chmod,d_t,user,host,pw,is_wgo):

    if is_wgo.lower() == "with grant option":
        is_wgo = 1
    else:
        is_wgo = 0

    write_row = []
    write_row.append(user)
    write_row.append(host.lower())
    write_row.append(pw)
    write_row.append(d_t)


    if "all privileges" in chmod.lower() or "all" in chmod.lower():
        for i in range(6):
            write_row.append(1)
        write_row.append(is_wgo)
        with open(userfile,"a",newline="") as csvfile:
            writer = csv.writer(csvfile,delimiter="|")
            writer.writerow(write_row)
        return 
    
    if "create" in chmod.lower():
        write_row.append(1)
    else:
        write_row.append(0)
    
    if "drop" in chmod.lower():
        write_row.append(1)
    else:
        write_row.append(0)

    if "insert" in chmod.lower():
        write_row.append(1)
    else:
        write_row.append(0)

    if "delete" in chmod.lower():
        write_row.append(1)
    else:
        write_row.append(0)

    if "update" in chmod.lower():
        write_row.append(1)
    else:
        write_row.append(0)

    if "select" in chmod.lower():
        write_row.append(1)
    else:
        write_row.append(0)

    write_row.append(is_wgo)

    with open(userfile,"a",newline="") as csvfile:
        writer = csv.writer(csvfile,delimiter="|")
        writer.writerow(write_row)

    return