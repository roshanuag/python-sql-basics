import pickle
a = ["a","b","c","d","e"]
d=open("lolz.dat","wb")

b=[]

for i in range(-1,-6,-1):
    b.append(a[i])
pickle.dump(b,d)
d.close()
with open("lolz.dat", "rb") as file :
    print(pickle.load(file))

