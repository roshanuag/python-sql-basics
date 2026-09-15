a = open("file1.txt","w")

for i in range(2):
    
    name = input("Enter name: ")

    a.write(name+"\n")

a.close()

