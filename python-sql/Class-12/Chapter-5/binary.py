import pickle
with open("dump.txt","wb+") as a:
    b=input("Enter a name: ")
    pickle.dump(b, a)

    