import mysql.connector
import re

connection = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "adminadmin",
    database = "vocab"
)

cursor = connection.cursor()
cursor.execute("SHOW DATABASES")
found = False

for db in cursor:
    pattern = "[(,')]"
    db_string = re.sub(pattern , "", str(db))
    if (db_string == 'vocab'):
        found = True
        print("Database vocab exists;")
if (not found):
    cursor.execute("CREATE DATABASE vocab")

sql = "DROP TABLE IF EXISTS vocab_table"
cursor.execute(sql)

sql = "CREATE TABLE vocab_table(word VARCHAR(255), definition VARCHAR(255) )"
cursor.execute(sql)

file = open("Vocabulary_list.csv", 'r')
words_list = file.readlines()
words_list.pop(0)

vocab_list = []

for word_string in words_list:
    word, definition = word_string.split(',',1)
    definition = definition.rstrip()
    vocab_list.append({word, definition})

    sql = "INSERT INTO vocab_table(word, definition) VALUES(%s, %s);"
    values = (word,definition)
    cursor.execute(sql, values)
    connection.commit()
    # print("Inserted " + str(cursor.rowcount) + " row into vocab_table") 

sql = "SELECT * FROM vocab_table WHERE word = %s"
value = ('boisterous', )
cursor.execute(sql, value)

result = cursor.fetchall()

for row in result:
    print(row)

sql = "UPDATE vocab_table SET definition =  %s WHERE word = %s" 
value = ("spirited; lively", "boisterous")
cursor.execute(sql, value)
connection.commit()
print("Modified row count: ", cursor.rowcount)

sql = "SELECT * FROM vocab_table WHERE word = %s"
value = ('boisterous', )
cursor.execute(sql, value)

result = cursor.fetchall()

for row in result:
    print(row)
