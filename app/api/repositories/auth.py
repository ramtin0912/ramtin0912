from flask import jsonify, json, request, Response
from datetime import datetime, timedelta
from app.api.serializers import LoginInputSchema
from app.services.db_helper import get_BasicInfoByUsername, IsAdmin, add_User
import jwt
import config

# ///////////////////////////////////////////////////
# Login

def LoginUser():

    data = json.loads(request.data)

    schema = LoginInputSchema()
    if schema.validate(data):
        return "Input is Invalid", 422

    input = schema.dump(schema.load(data))

    user = get_BasicInfoByUsername(input["username"])
    
    if user == None:
        return 'User does not exist'

    if user["Username"] != input["username"] or user["Username"] != input["username"]:
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = jwt.encode({'username' : user["Username"], 'exp' : datetime.utcnow() + timedelta(hours = 1)}, config.SECRET_KEY, "HS256")

    resp = Response()
    resp.headers['authorization'] = access_token
    return resp

    #return redirect(url_for("/users/"))

# Admin login

def LoginAdmin():

    data = json.loads(request.data)

    schema = LoginInputSchema()
    if schema.validate(data):
        return "Input is Invalid", 422

    input = schema.dump(schema.load(data))

    isAdmin = IsAdmin(input["username"])

    if isAdmin["IsAdmin"] == 0:
        return 'This user is not autherized'

    user = get_BasicInfoByUsername(input["username"])

    if user == None:
        return 'User does not exist'

    if user["Username"] != input["username"] or user["Username"] != input["username"]:
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = jwt.encode({'username' : user["Username"], 'exp' : datetime.utcnow() + timedelta(hours = 1)}, config.SECRET_KEY, "HS256")


    resp = Response()
    resp.headers['authorization'] = access_token
    return resp

    #return redirect(url_for("/api/users/"))

# Register

def Register():
            
    data = json.loads(request.data)

    schema = LoginInputSchema()
    if schema.validate(data):
        return "Input is Invalid", 422

    input = schema.dump(schema.load(data))

    user = get_BasicInfoByUsername(input["username"])

    inputForm = {
        "password": input["password"],
        "username": input["username"],
        "balance": 0,
        "is_admin": False
    }

    if user is None:
        add_User(inputForm)
            
        return '',204
    else:
        return 'This user already exists'
    
    #return redirect(url_for('api/users/'))
