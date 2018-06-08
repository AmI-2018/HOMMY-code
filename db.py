import mysql.connector
import random

userdb = 'root'
pswdb = 'asdf12345'
host = 'localhost'
db = 'hommy'

def chalQuery(query, n):
    if(n!=0):
        query = query + " WHERE id NOT IN (SELECT id FROM challenges WHERE id = %s"
        for i in range(1,n):
            query= query + " or id = %s"
        query = query +')'

    return query


def showCategories():
    conn = mysql.connector.connect(user=userdb, password=pswdb, host=host, database=db)
    query = "SELECT id, name, nChallenges, disabled FROM categories ORDER BY id"

    cursor = conn.cursor()
    cursor.execute(query)

    result = cursor.fetchall()

    cursor.close()
    conn.close()
    return result


def getRandomChallenge(category, chal_list):
    chal = -1
    conn = mysql.connector.connect(user=userdb, password=pswdb, host=host, database=db)
    query1 = "SELECT nChallenges FROM categories WHERE name=%s"
    query2 = "SELECT id, name, description, type, trivia FROM hommy.challenges"
    query2 = chalQuery(query2, len(chal_list))

    c1 = conn.cursor()
    c1.execute(query1,(category,))
    nChal = int((c1.fetchone())[0]) - len(chal_list)
    c1.close()

    if nChal != 0:
        c2 = conn.cursor()
        rand = random.randint(1,nChal)
        if len(chal_list) == 0:
            c2.execute(query2)
        else:
            c2.execute(query2,tuple(chal_list))
        chal = c2.fetchall()
        chal = chal[rand-1]
        c2.close()

    conn.close()
    return chal

def getChallenge(id):
    conn = mysql.connector.connect(user=userdb, password=pswdb, host=host, database=db)
    query = "SELECT id, name, description, type, trivia FROM hommy.challenges WHERE id = %s"

    cursor = conn.cursor()
    cursor.execute(query, (id,))
    res = cursor.fetchone()

    cursor.close()
    conn.close()

    return res


def getRandomQuiz(id):
    conn = mysql.connector.connect(user=userdb, password=pswdb, host=host, database=db)
    query = "SELECT idChal, idQuestion, question, answer, wrong1, wrong2, wrong3 FROM triviachallenge WHERE idChal = %s"

    cursor = conn.cursor()
    cursor.execute(query, (id,))
    res = cursor.fetchall()
    rand = random.randint(1, len(res))
    res = res[rand-1]

    cursor.close()
    conn.close()

    return res


def getUserInfo(username, psw):
    conn = mysql.connector.connect(user=userdb, password=pswdb, host=host, database=db)
    query = "SELECT username, birthDate, genre, challengeWon, mostPlayedCat FROM profiles WHERE username = %s AND psw = %s"

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
    #getUserInfo("lorry03","asdf12345")
    #print(registerUser("lorry96", "abdullah", "1996-12-25", "M"))
    #print(getRandomChallenge("DEMO", [1,2]))
    #print(getRandomChallenge("DEMO", []))
    print(getRandomQuiz(4))

