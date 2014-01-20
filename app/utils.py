import dbscan

maxHits = 22

def mset(m, d, p):
    m[d]=p

# hitsWeight percent from 0-1.0
def getTopNWeighted(point, radius, n, hitsWeight):
    proxWeight = 1.0 - hitsWeight
    landmarks = dbscan.regionQuery(point, radius)
    m = {}
    [mset(m, dbscan.fDist(point, p), p) for p in landmarks]
    for p in landmarks:
        dist = dbscan.fDist(point, p)
        pScore = proxWeight * (1 - dist/radius)
        hScore = hitsWeight * (p.hits/maxHits)
        mset(m, pScore + hScore, p)
    sorted(m)
    vals = m.values()
    return vals[len(vals) - n:]

    
def getTopNProx(point, radius, n):
    landmarks = dbscan.regionQuery(point, radius)
    m = {}
    [mset(m, dbscan.fDist(point, p), p) for p in landmarks]
    sorted(m)
    return m.values()[0:n]
    
def getTopNHits(point, radius, n):
    landmarks = dbscan.regionQuery(point, radius)
    m = {}
    [mset(m, p.hits, p) for p in landmarks]
    sorted(m)
    vals = m.values()
    return vals[len(vals) - n:]

