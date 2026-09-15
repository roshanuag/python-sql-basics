user_input = input("Enter numbers separated by spaces(eg:10 112 2 3 5 6 etc): ")
alist = list(map(int, user_input.split()))
print("Original list", alist)
n = len(alist)
for i in range(n):
    for j in range(0 , n - i -1):
        if alist[j] > alist[j+1]:
            alist[j], alist[j + 1] = alist[j+1] , alist[j]
    print("Sorted List", alist)
