def count_chr(s):#function to check number of upper case and lower case in str s
    upper = lower = symbols = digits = 0 
    for char in s:
        if char.isupper():
            upper += 1
        elif char.islower():
            lower+=1
        elif char.isdigit():
            digits+=1
        else:
            symbols += 1
    print("Upper case:", upper)
    print("Lower case:", lower)#prints the number of lower case 
    print("Digits:", digits)
    print("Symbols:", symbols)

input_str = input("Enter a string:")#takes input string from user


count_chr(input_str)#calling the function

TOTAL_chr = len(input_str)#total length
print("Total characters:",TOTAL_chr)