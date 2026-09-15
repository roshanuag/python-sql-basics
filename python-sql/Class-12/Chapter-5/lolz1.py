source="lolz2.txt"
target="practice.txt"
with open("lolz2.txt","r") as a , open("practice.txt","w") as b:
    for line in a:
        if line.startswith("@"):
            b.write(line)