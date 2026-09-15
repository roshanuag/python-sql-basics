import csv
a = open("stu.csv","w",newline="")
b = csv.writer(a)

b.writerow(["Roll no", "Name", "Marks", "Sex"])

for i in range(10):
    print("Student record ",(i+1))
    rollno = int(input("Enter roll number: "))
    name = input("Enter student name: ")
    marks = float(input("Enter student marks: "))
    sex = input("Enter your sex: ")
    
    student_record = [rollno, name, marks, sex]
    b.writerow(student_record)
a.close()