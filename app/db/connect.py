import mysql.connector
import json

json_data=open('app/db/config.json')
data = json.load(json_data)
json_data.close()
cur = None

def showTables(cur):
	# Use all the SQL you like
	execute('SHOW TABLES')
	# print all the first cell of all the rows
	for row in cur.fetchall():
		print row[0]

def getColNames(tbName):
	global cur
	rows = query('DESCRIBE ' + tbName)
	names=list()
	for name in rows:
		names.append(name[0])
	return names

def getTable(tbName, where=None):
	keys = getColNames(tbName)
	rows = getRows(tbName, keys, where)
	return {'keys':keys, 'rows':rows}

def getRows(tbl, keys, where):
	db = getDB()
	s = str()
	for k in keys:
		s += k + ','
	s = 'SELECT ' + s[:-1] + ' FROM ' + tbl
	if where:
		s += ' WHERE ' + where
	db.execute(s)
	close()
	return db.fetchall()

def insert(tbl, vals):
	vList = vals.values()

	sql = "INSERT INTO " + tbl + " (" + ','.join(map(lambda k: '`' + k + '`', vals.keys())) + ")"
	sql += " VALUES (" + dupString("%s", len(vList)) + ")"

	execute(sql, vList)

def updateRowValsWhere(tbl, vals, wVals):
	values = [tbl]

	sql = 'UPDATE %s SET '
	s, v = mapToSqlAndList(vals)
	values.append(v)

	# set Where clause
	sql = ' WHERE '
	s, v = mapToSqlAndList(vals, 'AND')
	values.append(v)

	execute(sql, values)

# update rows for rowID with dict vals
def updateRowVals(tbl, vals, rowID):
	values = [tbl]
	sql = 'UPDATE %s SET '
	s, v = mapToSqlAndList(vals)
	values.append(v)
	sql += s + ' WHERE id = %s'
	execute(sql, values)

def updateRowVal(tbl, field, val, rowID):
	execute('UPDATE %s SET %s=%s WHERE id=%s', [tbl,field,val,rowID])

def mapToSqlAndList(map, sep=','):
	values=list()
	for field, val in map.iteritems():
		sql += '%s=%s' + sep
		values.append(field)
		values.append(val)
	sql = sql[:-len(sep)]
	return sql, values

def dupString(s, times, sep=','):
	new = s
	while times != 1:
		new += sep + s
		times -= 1
	return new

def query(sql,values=None):
    global cur
    print sql
    if cur is None:
        getDB()
    if values:
        cur.execute(sql, values)
    else:
        cur.execute(sql)
    rows=cur.fetchall()
    close()
    return rows

def execute(sql,values=None, commitStmt=True):
	global cur
	if cur is None:
		getDB()
	if values:
		cur.execute(sql, values)
	else:
		cur.execute(sql)
	if commitStmt:
		commit()
	close()

def getDB():
	global db
	global cur
	db = mysql.connector.connect(
		host=data['mysql']['hostname'],
		user=data['mysql']['username'],
		password=data['mysql']['password'],
		database=data['mysql']['database'])

	cur = db.cursor()
	return cur

def commit():
	db.commit()

def close():
	db.close()
	global cur
	cur = None

