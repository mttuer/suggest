from flask import render_template, flash, redirect, request
from app import app
from db.connect import *
from db import utils
import learner 
import copy

links = [
    {'title': 'Home', 'view': 'index'}
    #{'title': 'Map', 'view': 'map'},
]

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Miguel'}
    return render_template('index.html',
            title = 'Home',
            links = links,
            user = user
    )

'''
@app.route('/music/reccomend', methods=['POST'])
def reccomend():
    insert('music', request.form)
    return render_template('common/picture_response.html')
'''

def jRet(val):
    ret =  "{\"result\": "
    if val:
        return ret + "true}"
    else:
        return ret + "false}"
    
@app.route('/users/new', methods=['POST'])
def createUser():
    if utils.createUser(request.form['email'], request.form['password']):
        return jRet(True)
    else:
        return jRet(False)

@app.route('/users/login', methods=['POST'])
def login():
    val = utils.login(request.form['email'], request.form['password'])
    return "{\"token\":" + val + "}"

@app.route('/users/tokenLogin', methods=['POST'])
def tokenLogin():
    token = utils.tokenLogin(request.form['token'])
    return jRet(token)

@app.route('/events/new', methods=['POST'])
def addEvent():
#TODO call some api to get genre from album id
    insert('music', request.form)
    # check for genre blacklist
    if request.form['skipped'] is not True:
        sqlD = "DELETE FROM genreBlacklists WHERE userID=%s AND genreID=%s"
        execute(sqlD, [request.form['userID'], request.form['genreID']])
    return render_template('common/picture_response.html')

#Blacklist genres until user listens to full song of that genre
@app.route('/events/shelf', methods=['POST'])
def shelfGenre():
    insert('genreBlacklists', [request.form['userID'], request.form['genreID']])
    return render_template('common/picture_response.html')

@app.route('/request/genre_recent', methods=['POST'])
def reccomendRecent():
    uid = request.form['userID']
    getMax = "SELECT MAX(id) FROM music WHERE userID = " + str(uid)
    cols = "time, date, X(position) AS lat, Y(posiition) AS lon, activity"
    qry = "SELECT " + cols + " FROM music WHERE id=(" + getMax + ")"
    rows = query(qry)
    mRec = {
    'userID':uid,
    'time':rows[0],
    'date':rows[1],
    'lat':rows[2],
    'lon':rows[3],
    'activity':rows[4]
    }
    return learner.getGenre(mRec)

@app.route('/request/genre', methods=['POST'])
def reccomendGenre(): 
    return learner.getGenre(request.form)


