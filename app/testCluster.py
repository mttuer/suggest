import numpy as np
import matplotlib.pyplot as plt
from db.connect import *
import dbscan
#from pylab import *
import pylab

def findNear():
    for p in dbscan.queryUnv():
        P = dbscan.getObjPoint(p)
        for cP in dbscan.regionQuery(P, 1):
            print cP

def printStuff():
# test object capture
    bearing = 350
    point = (0,1)
    focus = 3
    p = dbscan.Point(0, 0, 1, False, bearing, focus)
    x = [p.lon]
    y = [p.lat]
    for bearing in range(0,360):
        if bearing % 20 > 10:
            continue
        p = dbscan.Point(0, 0, 1, False, bearing, focus)
        P = dbscan.getObjPoint(p)
        x.append(P.lon)
        y.append(P.lat)
        color=['g','r']
        sql = "INSERT INTO pictures (position,visited,bearing,focus) VALUES (POINT(%s, %s), %s, %s, %s)"
        vals = [p.lat, p.lon, p.vis, bearing, focus]
        print 'Beginning new cluster', vals
        execute(sql, vals)

    pylab.scatter(x,y, s=100 ,marker='o', c=color)
    pylab.xlim(xmin=0)

def mapObjects():
    sql = "SELECT X(position), Y(position), focus, bearing FROM pictures;"
    rows = query(sql)
    x = list()
    y = list()
    for row in rows:
        p = dbscan.Point(0, row[1], row[0], True, row[3], row[2])
        P = dbscan.getObjPoint(p)
        x.append(P.lon)
        y.append(P.lat)
    pylab.scatter(x,y, s=100 ,marker='o')
    pylab.show()

def mapLandmarks():
    sql = "SELECT X(position), Y(position) FROM landmarks;"
    rows = query(sql)
    x = list()
    y = list()
    print len(rows)
    for row in rows:
        x.append(row[1])
        y.append(row[0])

    area = np.pi * .5**2
    plt.scatter(x, y, s=area, alpha=0.5)
    plt.show()

def mapPoints(P):
    x=list()
    y=list()
    for p in P:
        x.append(p.lat)
        y.append(p.lon)

    area = np.pi * .9**2
    plt.scatter(x, y, s=area, alpha=0.5)
    plt.show()

def mapTop(P, n):
    l = dbscan.getTopN(P, 5, n)
    l.append(P)
    mapPoints(l)

def testTop(P, n):
    for p in dbscan.getTopN(P, 5, n):
        print p, p.lat, p.lon

#findNear()
P = dbscan.Point(0,2,1,0,0,0) 
mapTop(P,3)

#dbscan.batchCluster()
#mapObjects()
#mapLandmarks()
#printStuff()

