from flask import jsonify, json, request
from datetime import datetime
from app.api.serializers import CreateUserFormSchema, UpdateUserFormSchema, UpdateUserBalanceFormSchema, ConfirmFormSchema, CreateTransactionFormSchema
from app.services.token_required import token_required
from app.services.db_helper import get_AllUsers, get_UserById, get_AllUserTransactions, add_User, update_UserInfo, add_Transaction, \
update_UserBalance, delete_UserById, delete_UserTransaction

# ADMIN REST API ////////////////////////////////////
# HTTP GET requests ---------------------------------
# Get a list of all users

@token_required
def GetAllUsers():

    Users = get_AllUsers()

    return jsonify(Users)

#Get the user with specific id

@token_required
def GetUserById(id):

    User = get_UserById(id)

    return jsonify(User)

# Get All users's transactions    

@token_required
def GetUserTransactions(id):

    Transactions = get_AllUserTransactions(id)
    
    return jsonify(Transactions)

# HTTP POST Requests ------------------------------------

@token_required
def CreateUser():

    data = json.loads(request.data)

    schema = CreateUserFormSchema()
    if schema.validate(data):
        return "Input is Invalid", 422

    input = schema.dump(schema.load(data))

    allUsers = get_AllUsers()

    for User in allUsers:
        if input["username"] == User["Username"]:
            return "Username alread taken", 400

    add_User(input)

    return '',204


@token_required
def SetTransaction(id):

    data = json.loads(request.data)

    schema = CreateTransactionFormSchema()
    if schema.validate(data):
        return "Input is Invalid", 422

    input = schema.dump(schema.load(data))

    User = get_UserById(id)

    if User["Balance"] < input["amount"] and input["type"] == 0:
        return 'User does not have enough funds'

    if input["type"] == 0:
        rest = (User["Balance"]) - input["amount"]
    else:
        rest = (User["Balance"]) + input["amount"]
    
    inputUserForm = {
        "balance" : rest,
        "id" : id
    }

    update_UserBalance(inputUserForm)

    print(datetime.utcnow())

    inputTransactionForm = {
        "user_id" : id,
        "amount" :  input["amount"],
        "type" : input["type"],
        "time" : datetime.utcnow()
    }

    add_Transaction(inputTransactionForm)
    
    return '',204

# HTTP PUT Requests ---------------------------------------

@token_required
def UpdateUser(id):

    User = get_UserById(id)

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
            return "Username already taken", 400

    inputForm = {
        "username" : newUser["username"],
        "password" : newUser["password"],
        "id" : id
    }

    update_UserInfo(inputForm)
    
    return '',204

# HTTP PATCH Requests ------------------------------

@token_required
def UpdateUserBalance(id):

    data = json.loads(request.data)

    schema = UpdateUserBalanceFormSchema()
    if schema.validate(data):
        return "Input is Invalid", 422

    input = schema.dump(schema.load(data))
    
    inputForm = {
        "balance" : input["balance"],
        "id" : id
    }

    update_UserBalance(inputForm)
    
    return '',204

# HTTP Delete Requests ---------------------------------------

@token_required
def DeleteUser(id):

    data = json.loads(request.data)

    schema = ConfirmFormSchema()
    if schema.validate(data):
        return "Input is Invalid", 422

    input = schema.dump(schema.load(data))

    if input["confirm"] == "confirm":

        delete_UserById(id)
        return '', 204

    return "Please confirm deletion", 400
    

@token_required
def DeleteUserTransaction(t_id, id):

    data = json.loads(request.data)
    
    schema = ConfirmFormSchema()
    if schema.validate(data):
        return "Input is Invalid", 422

    input = schema.dump(schema.load(data))

    if input["confirm"] == "confirm":

        input_form = {
            "user_id" : id,
            "id" : t_id
        }

        delete_UserTransaction(input_form)
        return '', 204

    return "Please confirm deletion", 400