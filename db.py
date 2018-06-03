import mysql.connector
import random
import webbrowser as wb
import time

userdb = 'root'
pswdb = 'asdf12345'
host = 'localhost'
db = 'hommy'

def showCategories():
    conn = mysql.connector.connect(user=userdb, password=pswdb, host=host, database=db)
    query = "SELECT id, name, nChallenges, disabled FROM categories ORDER BY id"

    cursor = conn.cursor()
    cursor.execute(query)

    result = cursor.fetchall()

    cursor.close()
    conn.close()
    return result

def getChallenge(category):
    conn = mysql.connector.connect(user=userdb, password=pswdb, host=host, database=db)
    query1 = "SELECT nChallenges FROM categories WHERE name=%s"
    query2 = "SELECT id, name, description, type FROM hommy.challenges WHERE id = %s"

    cursor = conn.cursor()
    cursor.execute(query1,(category,))
    nChal = int((cursor.fetchone())[0])
    rand = random.randint(1,nChal)
    cursor.execute(query2,(rand,))
    chal = cursor.fetchone()

    cursor.close()
    conn.close
    return chal

def getChallenge2(id):
    conn = mysql.connector.connect(user=userdb, password=pswdb, host=host, database=db)
    query = "SELECT id, name, description, type FROM hommy.challenges WHERE id = %s"

    cursor = conn.cursor()
    cursor.execute(query, (id,))
    res =  cursor.fetchone()

    cursor.close()
    conn.close

    return res

def getUserInfo(username, psw):
    conn = mysql.connector.connect(user=userdb, password=pswdb, host=host, database=db)
    query = "SELECT username, age, genre, challengeWon, mostPlayedCat FROM profiles WHERE username = %s AND psw = %s"

    cursor = conn.cursor()
    cursor.execute(query,(username,psw))
    res = cursor.fetchone()

    cursor.close()
    conn.close()
    return res

def registerUser(username, psw, date, genre):
    conn = mysql.connector.connect(user=userdb, password=pswdb, host=host, database=db)
    query = "INSERT INTO profiles (username, psw, birthDate, genre) VALUES (%s, %s, %s, %s)"

    cursor = conn.cursor()
    try:
        cursor.execute(query, (username, psw, date, genre))
        conn.commit()
    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()
        return "USER ALREADY EXIST"

    cursor.close()
    conn.close()
    return "SUCCESS"



if __name__ == '__main__':
    """res= showCategories()
    print(res)
    getChallenge("DEMO")
    url= 'file:///D:/lorry/Documents/Atom/Repo%20Hommy/HOMMY/index.html'
    wb.open(url)
    time.sleep(3)
    wb.open("https://www.google.it")"""

    #getUserInfo("lorry03","asdf12345")
    print(registerUser("lorry96", "abdullah", "1996-12-25", "M"))

