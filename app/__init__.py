import os
from flask import Flask
from db.tables import createAll
app = Flask(__name__)
createAll()
print "Config"
app.config.from_object('config')
print "Begin view"
from app import views

