a = open("file2.txt","a")

l = []

for x in range(2):

    name = input("Enter name: ")

    l.append(name+"\n")

a.writelines(l)

a.close()
