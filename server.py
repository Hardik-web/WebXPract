
from bson import ObjectId
from flask import Flask, Response, request
import pymongo
import json
# from bson.objectid import ObjectId
app = Flask(__name__)

try:
    mongo=pymongo.MongoClient(host="localhost",port=27017,serverSelectionTimeoutMS=1000)
    db=mongo.company
    mongo.server_info()
except:
    print("errrrror")

@app.route("/users",methods=["GET"])
def get_users():
    try:
        data=list(db.users.find())
        for user in data:
            user['_id']=str(user["_id"])
        return Response(
             response=json.dumps(data),
             status=200,
             mimetype="application/json"
         )


    except Exception as ex:
         print(ex)
         return Response(
             response=json.dumps({"mess":"cannot read user"}),
             status=500,
             mimetype="application/json"
         )
@app.route("/users",methods=['POST'])
def create_user():
     try:
         user={"name":request.form['name'],"lastname":request.form['lastname']}
         dbResponse=db.users.insert_one(user)
         print(dbResponse.inserted_id)
         return Response(
             response=json.dumps({"name":"hardik","id":f"{dbResponse.inserted_id}"}),
             status=200,
             mimetype="application/json"
         )
     except Exception as ex:
         print(ex)

@app.route('/users/<id>',methods=['PATCH'])
def update(id):
    try:
        dbResponse=db.users.update_one(
            {"_id":ObjectId(id)},
            {"$set":{"name":request.form["name"]}}
        )
        if dbResponse.modified_count==1:
            return Response(
             response=json.dumps({"mess":"user updates"}),
             status=200,
             mimetype="application/json"
         )
        else:
            return Response(
             response=json.dumps({"mess":"nothing to updates"}),
             status=200,
             mimetype="application/json"
         )

        
    except Exception as ex:
         print(ex)
         return Response(
             response=json.dumps({"mess":"cannot update"}),
             status=500,
             mimetype="application/json"
         )


@app.route('/users/<id>',methods=['DELETE'])
def delete(id):
    try:
        dbResponse=db.users.delete_one(
            {"_id":ObjectId(id)},


        )
        return Response(
            response=json.dumps({"mess":"user deleted","id":f"{id}"}),
            status=200,
            mimetype="application/json"
         )
       

        
    except Exception as ex:
         print(ex)
         return Response(
             response=json.dumps({"mess":"cannot delete"}),
             status=500,
             mimetype="application/json"
         )
    
    

if __name__=='__main__':
    app.run(port=80,debug=True)