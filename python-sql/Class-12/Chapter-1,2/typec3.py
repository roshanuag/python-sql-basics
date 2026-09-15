
l = list(map(int, input("Enter list: ").split()))

m = list(map(int, input("Enter list: ").split()))

if len(l) != len(m):

    print("Error: Lists must be of the same length.")
else:
    n = [l[i] + m[i] for i in range(len(l))]
print("Resultant list n (sum of corresponding elements):", n)
