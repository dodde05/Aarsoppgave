import mysql.connector as mariadb

conn = mariadb.connect(
    host="10.2.2.153",
    user="client",
    password="79E76w864dcKbja",
    database="highscores"
    )

navn = input("Oppgi ditt kallenavn: ")
highscore = input("Din highscore ble: ")

cursor = conn.cursor()

query = f"INSERT INTO attempt (navn, score, dato) VALUES ('{navn}', {highscore}, CURDATE())"
cursor.execute(query)

conn.commit()

print(cursor.rowcount, "record inserted")