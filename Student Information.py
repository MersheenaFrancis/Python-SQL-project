import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",              # or your username
    password="Rowdy@26", # replace with your MySQL password
    database="studentdb"  # replace with your database name
)

# Create a cursor object
cursor = conn.cursor()

# Example: Fetch the current database
sql = """INSERT INTO details (Student_ID,Student_name,Age,DOB,Location) VALUES (%s,%s,%s,%s,%s)"""

values = (5,"Das",20,"2005-08-05","Coimbatore")

cursor.execute(sql,values)
conn.commit()


print("Data innserted sucessfuully! ")

# Close the connection
cursor.close()
conn.close()
