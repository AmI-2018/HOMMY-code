from selenium import webdriver as wd
driver = wd.Firefox()
THIS_SERVER = "http://192.168.1.111:5000"


def categories():
    driver.get(THIS_SERVER + "/categories")


def challenge(chal_id):
    driver.get(THIS_SERVER + "/viewChallenge/" + chal_id)


def players():
    driver.get(THIS_SERVER + "/players")


def endGame():
    driver.get(THIS_SERVER + "/endgame")