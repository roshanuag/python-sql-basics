target_roll_nos={12,14}
try:
    with open("stu.dat","r") as file:
        found = False

        for line in file:
            parts = line.strip().split(",")

            if parts:
                try:
                    roll_no = int(parts[0])
                    if roll_no in target_roll_nos:
                        print("Record found: ", line.strip())
                        found = True
                except ValueError:
                    print("invalid")
        if not found:
            print("no records")
except FileNotFoundError:
    print("no file")