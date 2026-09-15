l = float(input("Enter a limit: "))
mp = 0
np = float(input("Enter the next price or 0 to stop: "))
while np>0:
    if np < l and np > mp:
        mp = np
    np = float(input("Enter next price or 0 to stop: "))
if mp >0:
    print(mp)
else:
    print("No price is below the limit!")