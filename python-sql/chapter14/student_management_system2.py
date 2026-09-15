from db import get_connection

def run_query(query, params=None, fetch=False):
    conn, cursor = get_connection()
    if not conn:
        return None
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params or ())
    data = cursor.fetchall() if fetch else None 
    conn.commit()
    cursor.close()
    conn.close()
    return data

# ---------------- TABLE SETUP FUNCTIONS ----------------
def create_students_table():
    run_query("""
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            class VARCHAR(50) NOT NULL,
            roll_no INT,
            percentage FLOAT,
            result VARCHAR(20),
            UNIQUE(roll_no, class)
        )
    """)
    print("✅ Students table created (if not already exists).")


# ---------------- STUDENT FUNCTIONS ----------------
def add_student():
    name = input("Enter student name: ").title()
    class_name = input("Enter student class: ")
    roll_no = input("Enter roll number: ")
    percentage = float(input("Enter percentage: "))
    result = "PASS" if percentage >= 33 else "FAIL"

    existing = run_query("SELECT * FROM students WHERE roll_no=%s AND class=%s", (roll_no, class_name), fetch=True)
    if existing:
        print("❌ Student with this roll number already exists in the class!")
        return

    run_query(
        "INSERT INTO students(name,class,roll_no,percentage,result) VALUES (%s, %s, %s, %s, %s)",
        (name, class_name, roll_no, percentage, result)
    )
    print(f"✅ Student added successfully. Result = {result}")

def edit_student():
    student_id = input("Enter student ID to edit: ")
    student = run_query("SELECT * FROM students WHERE id=%s", (student_id,), fetch=True)

    if not student:
        print("❌ No student found with that ID.")
        return

    print(f"Editing student: {student[0]['name']} (Class {student[0]['class']}, Roll {student[0]['roll_no']})")


    new_name = input("Enter new name (leave blank to keep current): ") or student[0]['name']
    new_class = input("Enter new class (leave blank to keep current): ") or student[0]['class']
    new_roll = input("Enter new roll no (leave blank to keep current): ") or student[0]['roll_no']
    new_percentage = input("Enter new percentage (leave blank to keep current): ") or student[0]['percentage']

    new_percentage = float(new_percentage)
    new_result = "PASS" if new_percentage >= 33 else "FAIL"

    run_query(
        "UPDATE students SET name=%s, class=%s, roll_no=%s, percentage=%s, result=%s WHERE id=%s",
        (new_name, new_class, new_roll, new_percentage, new_result, student_id)
    )
    print("✅ Student updated successfully.")

def view_student():
    print("\n--- View Students ---")
    print("1. View All Students")
    print("2. View Specific Student")
    choice = input("Enter choice: ")

    if choice == "1":
        students = run_query("SELECT * FROM students", fetch=True)
        print("\n📌 Students List:")
        if not students:
            print("No students found!!")
        else:
            for s in students:
                print(f"ID:{s['id']}, Name:{s['name']}, Class:{s['class']}, Roll No:{s['roll_no']}, "
                      f"Percentage:{s['percentage']}, Result:{s['result']}")

    elif choice == "2":
        sid = input("Enter Student ID: ")
        student = run_query("SELECT * FROM students WHERE id=%s", (sid,), fetch=True)
        if not student:
            print("❌ Student not found!")
        else:
            s = student[0]
            print(f"\nID:{s['id']}, Name:{s['name']}, Class:{s['class']}, Roll No:{s['roll_no']}, "
                  f"Percentage:{s['percentage']}, Result:{s['result']}")


def delete_student():
    student_id = input("Enter student ID to delete: ")
    run_query("DELETE FROM students WHERE id=%s", (student_id,))
    print("✅ Student deleted successfully.")
def add_column():
    col_name = input("Enter new column name: ")
    col_type = input("Enter column type (e.g. VARCHAR(50), INT, FLOAT): ")
    try:
        run_query(f"ALTER TABLE students ADD COLUMN {col_name} {col_type}")
        print(f"✅ Column '{col_name}' added successfully.")
    except Exception as e:
        print("❌ Error:", e)

def drop_column():
    col_name = input("Enter column name to drop: ")
    try:
        run_query(f"ALTER TABLE students DROP COLUMN {col_name}")
        print(f"✅ Column '{col_name}' dropped successfully.")
    except Exception as e:
        print("❌ Error:", e)

def rename_column():
    old_name = input("Enter current column name: ")
    new_name = input("Enter new column name: ")
    new_type = input("Enter column type (must specify, e.g. VARCHAR(50), INT): ")
    try:
        run_query(f"ALTER TABLE students CHANGE {old_name} {new_name} {new_type}")
        print(f"✅ Column '{old_name}' renamed to '{new_name}' successfully.")
    except Exception as e:
        print("❌ Error:", e)

def modify_column_type():
    col_name = input("Enter column name to modify: ")
    new_type = input("Enter new column type (e.g. FLOAT, VARCHAR(100)): ")
    try:
        run_query(f"ALTER TABLE students MODIFY {col_name} {new_type}")
        print(f"✅ Column '{col_name}' type changed to {new_type}.")
    except Exception as e:
        print("❌ Error:", e)

def show_table_structure():
    structure = run_query("DESCRIBE students", fetch=True)
    print("\n📌 Current Students Table Structure:")
    for col in structure:
        print(f"- {col['Field']} ({col['Type']})")

def setup_menu():
    while True:
        print("\n--- Table Setup Menu ---")
        print("1. Create Students Table")
        print("2. Add Column")
        print("3. Drop Column")
        print("4. Rename Column")
        print("5. Modify Column Type")
        print("6. Show Table Structure")
        print("7. Back to Main Menu")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            create_students_table()
        elif choice == "2":
            add_column()
        elif choice == "3":
            drop_column()
        elif choice == "4":
            rename_column()
        elif choice == "5":
            modify_column_type()
        elif choice == "6":
            show_table_structure()
        elif choice == "7":
            break
        else:
            print("❌ Invalid choice, try again.")


# ---------------- MAIN MENU ----------------
while True:
    print("\n--- Student Management System ---")
    print("1. Add Student")
    print("2. View Students")
    print("3. Delete Student")
    print("4. Create Students Table")
    print("5. Edit Student")
    print("6. Edit Table")
    print("7. Exit")

    ui = input("\nEnter your choice: ")

    if ui == "1":
        add_student()
    elif ui == "2":
        view_student()
    elif ui == "3":
        delete_student()
    elif ui == "4":
        create_students_table()
    elif ui =="5":
        edit_student()
    elif ui == "6":
        setup_menu()
    elif ui == "7":
        print("👋 Exiting System...")
        break
    else:
        print("❌ Invalid choice, try again.")
