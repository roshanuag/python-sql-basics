# import mysql.connector
# db_config = { 
#     "host":"localhost",
#     "user":"root",
#     "password":"ttzq8005",
#     "database":"roshan"
#     }
# def get_connection():
#     try:
#         conn = mysql.connector.connect(**db_config)
#         cursor = conn.cursor(dictionary=True)
#         return conn, cursor
#     except mysql.connector.Error as e:
#         print(f"[DB ERROR] {e}")
#         return None, None

import mysql.connector

conn= mysql.connector.connect(host="localhost",user="root",password="ttzq8005",database="roshan")

cursor = conn.cursor()
cursor.execute("create database lolz")



conn.close()