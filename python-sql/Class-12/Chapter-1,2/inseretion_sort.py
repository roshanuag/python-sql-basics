alist = [15,6,13,22,3,52,2]
print("Original list", alist)

n = len(alist)
for i in range(1 , n):
    key = alist[i]
    j = i-1
    
    while j >=0 and key < alist[j]:
        alist[j+1]=alist[j]
        j = j-1
    else:
        alist[j+1]=key
print('Sorted List', alist)