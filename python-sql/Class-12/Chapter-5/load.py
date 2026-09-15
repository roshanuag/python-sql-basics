import pickle
a = open("abc1.dat", "rb")
y="my name is ram"
c= pickle.load(a)
print(c)
a.close()

