a = input("Enter a phone number:")
b = len(a)
if a[3] == "-" and a[7]=="-" and b == 12:
    print(a , "is a legal input")