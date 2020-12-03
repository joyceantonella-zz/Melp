#Just a dumb test
from math import radians, cos, sin, asin, sqrt
import statistics
from flask import Flask 
from flask import jsonify
from flask import request
import MySQLdb
import json


vHost   = "localhost"
vUser   = "root"
vPasswd = "admin123"
vDb     = "melp_test"
vTable  = "Restaurants"

db = MySQLdb.connect(host=vHost,   
                     user=vUser,        
                     passwd=vPasswd,  
                     db=vDb)        

cur = db.cursor()




def read(id=None):
	response = []
	query = "SELECT *FROM %s" %(vTable) 
	if(id is not None):
		query = query+" WHERE id ='%s'" %(id)

	
	resp = cur.execute(query)
	retrieved = cur.fetchall();
	headers = [x[0] for x in cur.description]
	for row in retrieved:
		response.append(dict(zip(headers, row)))

	return json.dumps(response, ensure_ascii=False).encode('utf8')



def delete(id):
	response = []
	resp = cur.execute("DELETE FROM %s WHERE id = '%s'" %(vTable, id))
	db.commit()
	resp2 = cur.execute("SELECT * FROM %s WHERE id = '%s'" %(vTable, id))
	if(resp==0):
		return "El id no existe", 400
	elif(resp2==1):
		return "No se ha realizado la operacion", 500
	else: return "success", 200 


def update(id, content):
	response = []
	update =""
	for key in content.keys():
		if(isinstance(content[key], str)):
			update = update+key+"='"+str(content[key])+"'," 
		else:
			update = update+key+"="+str(content[key])+","

	update = update[0:-1]
	query = "UPDATE %s SET %s WHERE id='%s'" %(vTable, update, id)
	resp = cur.execute(query)
	if(resp==0):
		return "El id no existe", 400
	elif(resp==1):
		return "success", 200
	


def create(content):
	response = []
	keys=""
	values =""
	for key in content.keys():
		keys   = keys+key+","
		if(isinstance(content[key], str)):
			values = values+"'"+content[key]+"'," 
		else:
			values = values+str(content[key])+","

	query = "INSERT INTO %s (" %(vTable)
	query = query+keys[:-1]+") VALUES("+values[:-1]+")"
	resp = cur.execute(query)
	db.commit()

	if(resp==1):
		return "success", 200
	else:
		return "no se ha realizado la operacion", 500



def checkDistance(centerlat, centerlon, lat, lon):
	centerlon, centerlat, lon, lat = map(radians, [centerlon, centerlat, lon, lat])
	earth = 6371
	dlon = lon - centerlon 
	dlat = lat - centerlat 
	a = sin(dlat/2)**2 + cos(centerlat) * cos(lat) * sin(dlon/2)**2
	c = 2 * asin(sqrt(a)) 
    
	return c * earth




def getInformation(latitude, longitude, radius):
	radius = radius/100
	torate = []

	query = "SELECT rating, lat, lng FROM %s" %(vTable)
	resp = cur.execute(query)

	retrieved = cur.fetchall()

	for row in retrieved:
		test = checkDistance(latitude, longitude, row[1], row[2])
		if(test <= radius):
			torate.append(row[0])

	if(len(torate)>0):
		response = {"count": len(torate), "avg": statistics.mean(torate), "std": statistics.stdev(torate)}
		return json.dumps(response)
	else:
		return "no se han encontrado restaurantes", 200
	




app = Flask(__name__) 
@app.route("/") 
def crud_readAll():
	return read()

@app.route("/<id>")
def crud_read(id):
	return read(id)

@app.route("/delete/<id>")
def crud_delete(id):
	return delete(id)

@app.route("/edit/<id>", methods=['GET', 'PUT'])
def crud_edit(id):
	content = request.get_json()
	return update(id, content)
	

@app.route("/create", methods=['GET', 'POST'])
def crud_create():
	content = request.get_json()
	return create(content)

@app.route("/restaurants/statistics", methods=['GET'])
def endpoint():
	latitude  = request.args.get('latitude', default=1, type=float)
	longitude = request.args.get('longitude', default=1, type=float)
	radius    = request.args.get('radius', default=1, type=float)

	return getInformation(latitude, longitude, radius)


if __name__ == '__main__':
	app.run(debug='True')
