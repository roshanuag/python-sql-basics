import mysql.connector
import hashlib
import csv
import os

# ==============================
# ✅ Database Configuration
# ==============================
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'ttzq8005',   
}

DB_NAME = 'roshan'

# ==============================
# ✅ Initialize DB & Tables
# ==============================
def init_db():
    conn = mysql.connector.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password']
    )
    cur = conn.cursor()
    cur.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    conn.commit()
    conn.close()

    conn = mysql.connector.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        database=DB_NAME
    )
    cur = conn.cursor()

    # Admin table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            username VARCHAR(50) PRIMARY KEY,
            password_hash VARCHAR(64) NOT NULL
        )
    """)

    # Students table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_id VARCHAR(50) UNIQUE NOT NULL,
            name VARCHAR(200) NOT NULL,
            class INT NOT NULL,
            dob VARCHAR(20),
            gender VARCHAR(20),
            address TEXT,
            phone VARCHAR(30)
        )
    """)

    # Results table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_id VARCHAR(50) NOT NULL,
            subject VARCHAR(100) NOT NULL,
            marks FLOAT,
            max_marks FLOAT,
            term VARCHAR(50),
            FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
        )
    """)

    cur.execute("SELECT * FROM admins WHERE username='admin'")
    if not cur.fetchone():
        default_pass = hashlib.sha256("admin123".encode()).hexdigest()
        cur.execute("INSERT INTO admins (username, password_hash) VALUES (%s,%s)", ("admin", default_pass))
        conn.commit()

    conn.close()
    print("✅ Database and tables initialized successfully.\n")

# ==============================
# ✅ Helper: Get DB connection
# ==============================
def get_db():
    return mysql.connector.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        database=DB_NAME
    )

# ==============================
# 👤 Admin Login
# ==============================
def admin_login():
    username = input("Enter admin username: ")
    password = input("Enter password: ")
    hashed = hashlib.sha256(password.encode()).hexdigest()

    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM admins WHERE username=%s AND password_hash=%s", (username, hashed))
    admin = cur.fetchone()
    db.close()

    return bool(admin)

# ==============================
# 🧍 Student Functions
# ==============================
def add_student():
    db = get_db()
    cur = db.cursor()

    student_id = input("Enter student ID: ")
    name = input("Enter full name: ")
    class_val = int(input("Enter class (1–12): "))
    dob = input("Enter date of birth (DD-MM-YYYY): ")
    gender = input("Enter gender: ")
    address = input("Enter address: ")
    phone = input("Enter phone number: ")

    cur.execute("""
        INSERT INTO students (student_id, name, class, dob, gender, address, phone)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, (student_id, name, class_val, dob, gender, address, phone))

    db.commit()
    db.close()
    print("✅ Student added successfully!\n")

def view_all_students():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT student_id, name, class, dob, gender, phone FROM students ORDER BY class, name")
    rows = cur.fetchall()
    db.close()

    print("\n--- All Students ---")
    for r in rows:
        print(r)
    print("--------------------\n")

def search_student():
    sid = input("Enter student ID to search: ")
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM students WHERE student_id=%s", (sid,))
    student = cur.fetchone()

    if student:
        print("\n📌 Student Details:")
        print(student)

        cur.execute("SELECT subject, marks, max_marks, term FROM results WHERE student_id=%s", (sid,))
        results = cur.fetchall()
        if results:
            print("\n📊 Results:")
            for r in results:
                print(r)
        else:
            print("\nNo results found.")
    else:
        print("❌ Student not found.")

    db.close()

def delete_student():
    sid = input("Enter student ID to delete: ")
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM students WHERE student_id=%s", (sid,))
    db.commit()
    db.close()
    print("✅ Student deleted if existed.\n")

# ==============================
# 📝 Results Functions
# ==============================
def add_result():
    db = get_db()
    cur = db.cursor()

    sid = input("Enter student ID: ")
    subject = input("Enter subject: ")
    marks = float(input("Enter marks obtained: "))
    max_marks = float(input("Enter max marks: "))
    term = input("Enter term (e.g. Term 1, Final): ")

    cur.execute("""
        INSERT INTO results (student_id, subject, marks, max_marks, term)
        VALUES (%s,%s,%s,%s,%s)
    """, (sid, subject, marks, max_marks, term))

    db.commit()
    db.close()
    print("✅ Result added.\n")

def view_class_results():
    class_val = int(input("Enter class to view results for: "))
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        SELECT s.student_id, s.name, r.subject, r.marks, r.max_marks, r.term
        FROM students s
        JOIN results r ON s.student_id = r.student_id
        WHERE s.class = %s
        ORDER BY s.name
    """, (class_val,))
    rows = cur.fetchall()
    db.close()

    print(f"\n📊 Results for Class {class_val}")
    for r in rows:
        print(r)
    print()

# ==============================
# 📤 Export to CSV
# ==============================
def export_students_to_csv():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()
    col_names = [desc[0] for desc in cur.description]

    with open("students_data.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(col_names)
        writer.writerows(rows)

    db.close()
    print("📁 Data exported to students_data.csv\n")
def change_admin_credentials():
    old_user = input("Enter current admin username: ")
    old_pass = input("Enter current password: ")
    old_hash = hashlib.sha256(old_pass.encode()).hexdigest()

    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM admins WHERE username=%s AND password_hash=%s", (old_user, old_hash))
    if not cur.fetchone():
        print("❌ Invalid old credentials.\n")
        db.close()
        return

    new_user = input("Enter new username: ")
    new_pass = input("Enter new password: ")
    new_hash = hashlib.sha256(new_pass.encode()).hexdigest()

    cur.execute("UPDATE admins SET username=%s, password_hash=%s WHERE username=%s", (new_user, new_hash, old_user))
    db.commit()
    db.close()
    print("✅ Admin credentials updated successfully!\n")

# ================================================
# 📄 Print Results - Classwise / Studentwise / All
# ================================================
def print_results():
    print("\n📄 Leave class/student ID empty to print all results\n")
    class_input = input("Enter class (leave blank for all): ").strip()
    student_input = input("Enter student ID (leave blank to print for entire class/school): ").strip()

    db = get_db()
    cur = db.cursor(dictionary=True)

    base_query = """
        SELECT s.student_id, s.name, s.class, r.subject, r.marks, r.max_marks, r.term
        FROM students s
        JOIN results r ON s.student_id = r.student_id
    """
    params = []

    # Filter based on input
    if class_input and student_input:
        base_query += " WHERE s.class = %s AND s.student_id = %s ORDER BY s.class, s.name, r.subject"
        params = [class_input, student_input]
    elif class_input:
        base_query += " WHERE s.class = %s ORDER BY s.class, s.name, r.subject"
        params = [class_input]
    elif student_input:
        base_query += " WHERE s.student_id = %s ORDER BY s.class, s.name, r.subject"
        params = [student_input]
    else:
        base_query += " ORDER BY s.class, s.name, r.subject"

    cur.execute(base_query, params)
    rows = cur.fetchall()
    db.close()

    if not rows:
        print("❌ No results found for the given input.\n")
        return

    # Group by student
    results_by_student = {}
    for row in rows:
        sid = row["student_id"]
        if sid not in results_by_student:
            results_by_student[sid] = {
                "name": row["name"],
                "class": row["class"],
                "results": []
            }
        results_by_student[sid]["results"].append(row)

    for sid, data in results_by_student.items():
        print("=" * 30)
        print("        SCHOOL RESULT")
        print("=" * 30)
        print(f"Student ID : {sid}")
        print(f"Name       : {data['name']}")
        print(f"Class      : {data['class']}")
        print("-" * 30)
        print(f"{'Subject':15} {'Marks/Max':>10}")
        print("-" * 30)
        total = 0
        max_total = 0
        for r in data["results"]:
            print(f"{r['subject']:15} {int(r['marks'])}/{int(r['max_marks'])}")
            total += r["marks"]
            max_total += r["max_marks"]
        print("-" * 30)
        print(f"Total: {int(total)} / {int(max_total)}")
        percent = (total / max_total) * 100 if max_total else 0
        print(f"Percentage: {percent:.2f} %")
        print("=" * 30 + "\n")

# ==============================
# 🏆 Topper from Each Class
# ==============================
def print_toppers_each_class():
    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute("""
        SELECT s.class, s.student_id, s.name,
               SUM(r.marks) AS total_marks,
               SUM(r.max_marks) AS total_max
        FROM students s
        JOIN results r ON s.student_id = r.student_id
        GROUP BY s.class, s.student_id
        ORDER BY s.class, total_marks DESC
    """)
    rows = cur.fetchall()
    db.close()

    if not rows:
        print("❌ No results available.\n")
        return

    # Find topper for each class
    toppers = {}
    for row in rows:
        c = row["class"]
        if c not in toppers:
            toppers[c] = row  # first row is topper due to ORDER BY

    print("\n🏆 Toppers of Each Class")
    print("=" * 40)
    print(f"{'Class':<8}{'Student ID':<12}{'Name':<20}{'%' :>5}")
    print("-" * 40)
    for c, t in toppers.items():
        percent = (t['total_marks'] / t['total_max']) * 100 if t['total_max'] else 0
        print(f"{c:<8}{t['student_id']:<12}{t['name']:<20}{percent:>5.2f}")
    print("=" * 40 + "\n")

def admin_menu():
    while True:
        print("""
========= ADMIN MENU =========
1. Add Student
2. View All Students
3. Search Student
4. Delete Student
5. Add Result
6. View Class Results
7. Export Students to CSV
8. Change Admin Credentials
9. Print Results (Student/Class/All)
10. Topper From Each Class
11. Logout
===============================
""")
        choice = input("Enter choice: ")

        if choice == "1": add_student()
        elif choice == "2": view_all_students()
        elif choice == "3": search_student()
        elif choice == "4": delete_student()
        elif choice == "5": add_result()
        elif choice == "6": view_class_results()
        elif choice == "7": export_students_to_csv()
        elif choice == "8": change_admin_credentials()
        elif choice == "9": print_results()
        elif choice == "10": print_toppers_each_class()
        elif choice == "11": break
        else: print("❌ Invalid choice\n")



# ==============================
# 🧠 Main Program
# ==============================
if __name__ == "__main__":
    init_db()

    while True:
        print("""
========= SCHOOL SYSTEM =========
1. Admin Login
2. Exit
=================================
""")
        ch = input("Enter choice: ")

        if ch == "1":
            if admin_login():
                admin_menu()
            else:
                print("❌ Login failed.\n")
        elif ch == "2":
            print("👋 Exiting...")
            break
        else:
            print("❌ Invalid choice\n")
