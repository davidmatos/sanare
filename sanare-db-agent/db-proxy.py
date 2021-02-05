import mysql.connector

mydb = mysql.connector.connect(
  host="10.1.0.99",
  user="wordpress",
  passwd="wordpress"
)

mycursor = mydb.cursor()

#mycursor.execute("SET GLOBAL log_output = 'TABLE';")

#mycursor.execute("SET GLOBAL general_log = 'ON';")


mycursor.execute("SELECT * FROM mysql.general_log;")

myresult = mycursor.fetchall()

for x in myresult:
    print(x)


