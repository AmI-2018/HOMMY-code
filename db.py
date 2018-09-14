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

def quizQuery(query, n):
    if(n!=0):
        query = query + " AND idQuestion NOT IN (SELECT idQuestion FROM triviachallenge WHERE idQuestion = %s"
        for i in range(1,n):
            query= query + " or idQuestion = %s"
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


"""def getRandomQuiz(id):
    conn = mysql.connector.connect(user=userdb, password=pswdb, host=host, database=db)
    query = "SELECT idChal, idQuestion, question, answer, wrong1, wrong2, wrong3 FROM triviachallenge WHERE idChal = %s"

    cursor = conn.cursor()
    cursor.execute(query, (id,))
    res = cursor.fetchall()
    rand = random.randint(1, len(res))
    #res = res[rand-1]

    cursor.close()
    conn.close()

    return res"""

def getRandomQuiz(id, quiz_list):
    conn = mysql.connector.connect(user=userdb, password=pswdb, host=host, database=db)
    query = "SELECT idChal, idQuestion, question, answer, wrong1, wrong2, wrong3, resource FROM triviachallenge WHERE idChal = %s"
    query = quizQuery(query, len(quiz_list))
    query2 = "SELECT COUNT(*) FROM triviachallenge"

    c1 = conn.cursor()
    """c2 = conn.cursor()
    
    c2.execute(query2)
    nQuiz = int((c2.fetchone())[0]) - len(quiz_list)
    c2.close()"""

    tmp = [id] + quiz_list
    c1.execute(query, tuple(tmp))
    res = c1.fetchall()
    rand = random.randint(1, len(res))
    res = res[rand-1]

    c1.close()
    conn.close()

    return res

def getUserInfo(username, psw):
    conn = mysql.connector.connect(user=userdb, password=pswdb, host=host, database=db)
    query = "SELECT username, birthDate, genre, challengeWon FROM profiles WHERE username = %s AND psw = %s"

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

def rate(chal_id, rate):
    conn = mysql.connector.connect(user=userdb, password=pswdb, host=host, database=db)
    query1 = "SELECT times, rate FROM challenges WHERE id = %s"
    query2 = "UPDATE challenges SET times = %s, rate = %s WHERE id = %s"

    cursor = conn.cursor()
    cursor.execute(query1, (chal_id,))
    res = cursor.fetchone()

    if res[1] is None:
        new_rate = rate
    else:
        new_rate = res[1] + rate
    times = res[0] + 1

    try:
        cursor.execute(query2, (times, new_rate, chal_id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()
        return "SOMETHING WENT WRONG"

    return "SUCCESS"

def getRanking(id):
    conn = mysql.connector.connect(user=userdb, password=pswdb, host=host, database=db)
    query = "SELECT username,bestScore FROM `profiles-challenges` WHERE idChal = %s ORDER BY bestScore DESC"

    cursor = conn.cursor()
    cursor.execute(query,(id,))
    res = cursor.fetchall()

    cursor.close()
    conn.close()
    return res

def bestScore(playerName, chal_id, score):
    conn = mysql.connector.connect(user=userdb, password=pswdb, host=host, database=db)
    query = "SELECT bestScore FROM `profiles-challenges` WHERE username = %s AND idChal = %s"

    cursor = conn.cursor()
    cursor.execute(query, (playerName,chal_id))
    res = cursor.fetchone()
    cursor.close()
    if res is None:
        query = "INSERT INTO `profiles-challenges`(username, idChal, bestScore) VALUES (%s, %s, %s)"
        cursor = conn.cursor()
        try:
            cursor.execute(query, (playerName, chal_id, score))
            conn.commit()
        except Exception as e:
            conn.rollback()
            cursor.close()
            conn.close()
            return "SOMETHING WENT WRONG"
    elif res[0] < score:
        query = "UPDATE `profiles-challenges` SET bestScore = %s WHERE username = %s AND idChal = %s"
        cursor = conn.cursor()
        try:
            cursor.execute(query, (score, playerName, chal_id))
            conn.commit()
        except Exception as e:
            conn.rollback()
            cursor.close()
            conn.close()
            return "SOMETHING WENT WRONG"
    return "SUCCESS"

if __name__ == '__main__':
    print(bestScore("lorry03", 1, 580))

