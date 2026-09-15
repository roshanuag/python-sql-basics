with open("lowerupper.txt","w") as a :
    a.write("hii i m python\nYOOObothsytgYUygy")
    a.close()

    with open("lowerupper.txt","r") as b:
        c=b.read()
        b.close()

        upper=lower=0

        for char in c:
            if char.isupper():
                upper+=1
            elif char.islower():
                lower+=1
        print("Uppercase letters:", upper)
        print("Lowercase letters:", lower)