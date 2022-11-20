from flask import *
import mysql.connector
#from flask import  Flask,render_template,jsonify,make_response

app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

mysql_pool=mysql.connector.pooling.MySQLConnectionPool(
            pool_name="mypool", pool_size=10, 
            host="localhost", database="taipei_attractions",
            user="debian-sys-maint", password="",
            pool_reset_session=True)

# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")

@app.route("/api/attractions")
def getAttractions():
	try:
		pageParameter=int(request.args.get("page",0)) 
	except ValueError as ex:
		print(ex)
		response = make_response(jsonify({"error":True,"message":"The page parameter you provied is not a digit."} ),400 )   
		response.headers["Content-Type"] = "application/json"
		return response

	keywordParameter=request.args.get("keyword","")
	if pageParameter<0:
		pageParameter=0
	dataCountPerPage=12
	
	try:
		conn = mysql_pool.get_connection() #get connection from connect pool
		cursor = conn.cursor()
		startId=pageParameter*dataCountPerPage
		
		if keywordParameter:
			keywordParameter=keywordParameter.replace("\"","")
			#check category
			sql='select id from category where name=%s'
			cursor.execute(sql,[keywordParameter])
			resultCategoryId = cursor.fetchone()
			
			dataAll=[]
			nextPage=pageParameter+1
			if resultCategoryId:
				#get id, name, description, address, transport, latitude, longitude, mrt, category
				sql='select json_object("id",attraction.id,"name",attraction.name,"description",attraction.description,"address",attraction.address,"transport",attraction.transport,"lat",attraction.latitude,"lng",attraction.longitude,"category",category.name,"mrt",mrt.name) from attraction left JOIN category ON attraction.category_id=category.id left JOIN mrt ON attraction.mrt_id=mrt.id where category_id=%s limit %s,%s'
				val=(resultCategoryId[0],startId,dataCountPerPage)
				cursor.execute(sql,val)
				resultFromAttraction= cursor.fetchall()
			else:
				#check attraction name
				#get id, name, description, address, transport, latitude, longitude, mrt, category
				sql='select json_object("id",attraction.id,"name",attraction.name,"description",attraction.description,"address",attraction.address,"transport",attraction.transport,"lat",attraction.latitude,"lng",attraction.longitude,"category",category.name,"mrt",mrt.name) from attraction left JOIN category ON attraction.category_id=category.id left JOIN mrt ON attraction.mrt_id=mrt.id where attraction.name like %s limit %s,%s'
				val=("%"+keywordParameter+"%",startId,dataCountPerPage)
				cursor.execute(sql,val)
				resultFromAttraction= cursor.fetchall()
			resultQuery={}
			for idx in range(0,dataCountPerPage):
				if idx>=len(resultFromAttraction):
					nextPage=None
					break		
				resultQuery.update(json.loads(resultFromAttraction[idx][0]))

				#get images
				sql='select imageUrl from image where attraction_id=%s'
				cursor.execute(sql,[resultQuery["id"]])
				resultImages = cursor.fetchall()
				getImages=[]
				for idx in range(0,len(resultImages)):
					getImages.append(resultImages[idx][0])
				resultQuery["images"]=getImages
				dataAll.append(resultQuery)

			if dataAll:
				response = make_response(jsonify({"nextPage":nextPage,"data":dataAll} ),200 ) 
			else:
				response = make_response(jsonify({"nextPage":None,"data":dataAll} ),200 ) 		
		else:	
			#total data
			sql='select count(id) from attraction'
			cursor.execute(sql)
			resultTotal= cursor.fetchone()	
			
			if startId>=resultTotal[0]:
				response = make_response(jsonify({"data":[],"nextPage":None}) ,200 ) 
			else:
				nextPage=pageParameter+1
				#get id, name, description, address, transport, latitude, longitude, mrt, category
				sql='select json_object("id",attraction.id,"name",attraction.name,"description",attraction.description,"address",attraction.address,"transport",attraction.transport,"lat",attraction.latitude,"lng",attraction.longitude,"category",category.name,"mrt",mrt.name) from attraction left JOIN category ON attraction.category_id=category.id left JOIN mrt ON attraction.mrt_id=mrt.id limit %s,%s'
				val=(startId,dataCountPerPage)
				cursor.execute(sql,val)
				resultFromAttraction= cursor.fetchall()
				
				dataAll=[]
				for idx in range(0,dataCountPerPage):
					if idx>=len(resultFromAttraction):
						nextPage=None
						break
					result={}
					result.update(json.loads(resultFromAttraction[idx][0]))
					#get images
					sql='select imageUrl from image where attraction_id=%s'
					cursor.execute(sql,[result["id"]])
					resultImages = cursor.fetchall()
					getImages=[]
					for idx in range(0,len(resultImages)):
						getImages.append(resultImages[idx][0])
					result["images"]=getImages
					dataAll.append(result)
				if dataAll:
					response = make_response(jsonify({"nextPage":nextPage,"data":dataAll} ),200 ) 
				else:
					response = make_response(jsonify({"nextPage":None,"data":dataAll} ),200 ) 
	except Exception as e:
		print(e)
		response = make_response(jsonify({"error":True,"message":"Can't connect to database."} ),500 )   
	finally:
		cursor.close()
		conn.close()
		response.headers["Content-Type"] = "application/json"
		return response
		

@app.route("/api/attraction/<attractionId>")
def getAttractionByAttractionId(attractionId):
	
	try:
		conn = mysql_pool.get_connection() #get connection from connect pool
		cursor = conn.cursor()
	except Exception as e:
		print(e)
		response = make_response(jsonify({"error":True,"message":"Can't connect to database."} ),500 )   
		response.headers["Content-Type"] = "application/json"
		cursor.close()
		conn.close()
		return response
	
	sql='select id from attraction where id=%s'
	cursor.execute(sql,[attractionId])
	checkAttractionIdValid = cursor.fetchone()
	if checkAttractionIdValid:
		resultQuery={}
		#get id, name, description, address, transport, latitude, longitude, mrt, category
		sql='select json_object("id",attraction.id,"name",attraction.name,"description",attraction.description,"address",attraction.address,"transport",attraction.transport,"lat",attraction.latitude,"lng",attraction.longitude,"category",category.name,"mrt",mrt.name) from attraction left JOIN category ON attraction.category_id=category.id left JOIN mrt ON attraction.mrt_id=mrt.id where attraction.id=%s'
		cursor.execute(sql,[attractionId])
		resultFromAttraction= cursor.fetchone()
		resultQuery.update(json.loads(resultFromAttraction[0]))
		#get images
		sql='select imageUrl from image where attraction_id=%s'
		cursor.execute(sql,[attractionId])
		resultImages = cursor.fetchall()
		getImages=[]
		for idx in range(0,len(resultImages)):
			getImages.append(resultImages[idx][0])
		resultQuery["images"]=getImages		
		response = make_response(jsonify({"data":resultQuery}),200 )   
	else:
		response = make_response(jsonify({"error":True,"message":"This attractionId is invalid."} ),400 )   
	cursor.close()
	conn.close()
	response.headers["Content-Type"] = "application/json"
	return response
	

@app.route("/api/categories")
def getCategories():
	try:
		conn = mysql_pool.get_connection() #get connection from connect pool
		cursor = conn.cursor()
		sql="select name from category"
		cursor.execute(sql)
		result = cursor.fetchall()
	except Exception as e:
		print(e)
		response = make_response(jsonify({"error":True,"message":"Can't connect to database."} ),500 )   
		response.headers["Content-Type"] = "application/json"
		return response
	finally:
		cursor.close()
		conn.close()

	if result:
		categories=[]		
		for idx in range(0,len(result)):
			categories.append(result[idx][0])
		response = make_response(jsonify({"data":categories} ),200 )   
		response.headers["Content-Type"] = "application/json"
		return response
	else:
		response = make_response(jsonify({"data":None} ),200 )  
		response.headers["Content-Type"] = "application/json"
		return response

app.run(host="0.0.0.0",port=3000)