with open("tell.txt", "w+") as a:

    b= input("Enter what u want to say: ")

    a.write(b)

    print("Here are few lines of what u said!!")

b = open("tell.txt", "r")

print(b.read(3))  

print(f"The fil pointer is at {b.tell()}")#tells the location of file pointer 

