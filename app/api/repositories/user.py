from flask import Flask, jsonify, request
from app.services.token_required import Usertoken_required
from datetime import timedelta, datetime
from app.api.serializers import CreateTransactionFormSchema, UpdateUserFormSchema
from app.services.db_helper import get_UserByUsername ,get_AllUserTransactionsByUsername ,update_UserBalance , \
add_Transaction, get_AllUsers, update_UserInfo, delete_UserById
import json
import jwt

# USERS REST API ////////////////////////////////////
# HTTP GET requests ---------------------------------
# Get users data

@Usertoken_required
def GetUserInfo(current_user):

    User = get_UserByUsername(current_user)

    return jsonify(User)

# Get All users's transactions    

@Usertoken_required
def GetUserTransactionsInfo(current_user):

    Transactions = get_AllUserTransactionsByUsername(current_user)
    
    return jsonify(Transactions)

# HTTP POST Requests ------------------------------------
# Make a Transaction

@Usertoken_required
def MakeTransaction(current_user):

    User = get_UserByUsername(current_user)

    data = json.loads(request.data)

    schema = CreateTransactionFormSchema()
    if schema.validate(data):
        return "Input is Invalid", 422

    input = schema.dump(schema.load(data))

    if User["Balance"] < input["amount"] and input["type"] == 0:
        return 'User does not have enough funds'

    if input["type"] == 0:
        rest = (User["Balance"]) - input["amount"]
    else:
        rest = (User["Balance"]) + input["amount"]
    
    inputUserForm = {
        "balance" : rest,
        "id" : User["ID"]
    }

    update_UserBalance(inputUserForm)

    inputTransactionForm = {
        "user_id" : User["ID"],
        "amount" :  input["amount"],
        "type" : input["type"],
        "time" : datetime.utcnow()
    }

    add_Transaction(inputTransactionForm)

    return '',204

# HTTP PUT Requests ---------------------------------------
# Update user basic

@Usertoken_required
def UpdateUserInfo(current_user):

    User = get_UserByUsername(current_user)

    if User == None:
        return "User does not exist", 400

    data = json.loads(request.data)

    schema = UpdateUserFormSchema()
    if schema.validate(data):
        return "Input is Invalid", 422

    newUser = schema.dump(schema.load(data))

    allUsers = get_AllUsers()

    for User in allUsers:
        if newUser["username"] == User["Username"]:
            return "Username alread taken", 400

    inputForm = {
        "username" : newUser["username"],
        "password" : newUser["password"],
        "id" : User["ID"]
    }

    update_UserInfo(inputForm)
    
    return '',204

# HTTP Delete Requests ---------------------------------------

@Usertoken_required
def SelfDelete(current_user):

    User = get_UserByUsername(current_user)

    data = json.loads(request.data)

    confirm = data['confirm']

    if confirm != "delete":
        return 'Please write delete to confirm deletion'

    delete_UserById(User["ID"])
    
    return '', 204
