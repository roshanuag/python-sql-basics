with open("seek.txt","w") as a :
    b = input("Enter what u want to say:")
    a.write(b)

b = open("seek.txt","r")
print(b.read(2))

b.seek(2,1)

print(b.read(2))