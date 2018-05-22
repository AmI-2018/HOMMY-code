import mysql.connector
import random

def showCategories():
    conn = mysql.connector.connect(user='root', password='asdf12345', host='localhost', database='hommy')
    query = "SELECT name, nChallenges FROM categories"

    cursor = conn.cursor()
    cursor.execute(query)

    result = cursor.fetchall()

    cursor.close()
    conn.close()
    return result


def getChallenge(category):
    conn = mysql.connector.connect(user='root', password='asdf12345', host='localhost', database='hommy')
    query1 = "SELECT nChallenges FROM categories WHERE name=%s"
    query2 = "SELECT id, name, type FROM hommy.challenges WHERE id = %s"

    cursor = conn.cursor()
    cursor.execute(query1,(category,))
    nChal = int((cursor.fetchone())[0])
    rand = random.randint(1,nChal)
    cursor.execute(query2,(rand,))
    chal = cursor.fetchone()
    return chal




if __name__ == '__main__':
    """res= showCategories()
    print(res)
    getChallenge("DEMO")"""