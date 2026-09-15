#DICT FUNCTIONS
a = {"1": "Rahul" , "2" : "ankit"}
print(len(a))#len function

b = a.clear()
print(b)#clear function

e = a.keys()#keys method
print(e)

f = a.values()#vale method
print(f)

dict1 ={"name": "roshan" , "salary": "10000" , "age": "26"}
dict2 = {"name" : "lavnish" , "salary": "10" , "dept": "sales"}

g = dict1.update(dict2)
print(dict1)
print(dict2)

c = dict1.get("age")
print(c)
d = dict1.items()