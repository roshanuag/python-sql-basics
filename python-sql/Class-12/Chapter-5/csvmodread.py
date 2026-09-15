import csv
with open("stu.csv","r") as a:
    b = csv.reader(a)
    for rec in b:
        print(rec)