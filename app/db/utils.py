import hashlib
import random
from connect import *
from datetime import datetime
import time

loggedIn = {}

def checkDateDif(d1, d2, minDif):
    d1_ts = time.mktime(d1.timetuple())
    d2_ts = time.mktime(d2.timetuple())
    if (d2_ts - d1_ts)/60.0 > 10:
        return False
    else:
        return True

def tokenLogin(token):
    global loggedIn
    if token not in loggedIn:
        return False
    else:
        d1 = loggedIn[token]
        d2 = datetime.now()
        ret = checkDateDif(d1, d2, 10)
        if ret: # Update token time
            loggedIn[token] = d2
        return ret

def containsEmail(email):
    sql = "SELECT id FROM users WHERE email=%s"
    rows = query(sql, [email])
    return len(rows) > 0
        
def createUser(email, password):
    if containsEmail(email):
        print "Email " + email + " already exists."
        return False
    random.seed()
    salt = random.getrandbits(31)
    salted = password + str(salt)
    hashVal = hash(salted)

    sql = "INSERT INTO users (email, password, salt) VALUES (%s, %s, %s)"
    execute(sql, [email, hashVal, salt])
    return True

def login(email, password):
    sql = "SELECT salt, password FROM users WHERE email=%s"
    rows = query(sql, [email])
    if len(rows) < 1:
        print "User does not exist"
        return "Failed"
    password += str(rows[0][0])
    hashVal = hash(password)
    if rows[0][1] == hashVal:
        random.seed()
        token = str(random.getrandbits(31))
        global loggedIn
        loggedIn[token] = datetime.now()
        return token
    return "Failed"

def deleteUser(email, password):
    if login(email, password):
        sql = "DELETE FROM users WHERE email=%s"
        execute(sql,[email])
        return True
    return False

def hash(password):
    hash_object = hashlib.sha256(password)
    return str(hash_object.hexdigest())

def unitTest():
    email = "mttuer@mtu.edu.oeiofnaoienaf"
    password = "password"
    assert containsEmail(email) is False, "This user already exists?"
    assert createUser(email, password) is True, "Failed to create user."
    token = login(email,password)
    assert token != "Failed", "Failed to login"
    assert tokenLogin(token) is True, "Failed to token login"
    assert tokenLogin("Fail") is False, "Failed to stop bad token login"
    assert login(email, "please fail") == "Failed",  "Failed to stop bad login"
    assert deleteUser(email, password) is True, "Failed to cleanup"

unitTest()


