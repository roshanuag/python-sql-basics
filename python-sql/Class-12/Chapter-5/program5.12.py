import pickle 
a = {}

b = open("load.txt", "rb")
try:
    print("load.txt has following data")
    while True:
        a = pickle.load(b)    
        print(b)
except EOFError:
    b.close()        
    