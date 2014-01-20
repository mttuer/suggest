import dbscan
import utils
utils.getTopNProx(dbscan.Point(0,1,1,True,1,1), 25, 10)
utils.getTopNHits(dbscan.Point(0,1,1,True,1,1), 25, 10)
utils.getTopNWeighted(dbscan.Point(0,1,1,True,1,1), 25, 10, .5)
