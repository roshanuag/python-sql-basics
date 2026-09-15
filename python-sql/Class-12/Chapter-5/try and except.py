a = open("try_expect.txt", "w")
b = input("What u want to say: ")
a.write(b)
a.close()


a = open("try_expect.txt", "r")
try:
    print(a.read(2))
except EOFError:
    a.close()