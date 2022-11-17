import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="dodde",
    password="BigMan!123",
    database="highscores"
)

navn = input("Oppgi dine initialer (3 bokstaver): ")
highscore = input("Din highscore ble: ")
dato = input("Dato (ÅÅÅÅ-MM-DD): ")

mycursor = mydb.cursor(navn, highscore, dato)

sql = "INSERT INTO attempt (initialer, score, dato) VALUES (%s, %s, %s)"
val = (navn, highscore, dato)
mycursor.execute(sql, val)

mydb.commit()

print(mycursor.rowcount, "record inserted.")