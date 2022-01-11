import mysql.connector
import config

def db_connector():
    try:
        connection = mysql.connector.connect(host=config.MYSQL_HOST, user=config.MYSQL_USERNAME,
                                             password=config.MYSQL_PASSWORD,
                                             database=config.MYSQL_DATABASE)
        if connection.is_connected():
            return connection
        else:
            raise Exception("can not connect to db")
    except Exception as e:
        raise e(422, "Error connecting to database")

def execute_query(query, data=None, connection=None, cursor=None, close_con=None):
    if connection is None and cursor is None:
        connection, cursor = open_db_connection()

    cursor.execute(query)
    result = None
    if data is not None:
        if data == "one":
            result = cursor.fetchone()
        else:
            result = cursor.fetchall()
    if close_con:
        commit_and_close_db_connection(connection, cursor)
    if result is not None:
        return result


def add_User(data):
    query = """INSERT INTO user 
            (Username, Password, Balance, IsAdmin) 
            VALUES ('{}', '{}', {}, {})""".format(data["password"], data["username"],
                                              data["balance"], data["is_admin"])
    return execute_query(query=query, close_con=True)


def add_Transaction(data):
    query = """INSERT INTO transaction 
            (User_id, Amount, Type, Time) 
            VALUES ({}, {}, {}, '{}')""".format(data["user_id"], data["amount"],
                                               data["type"], data["time"])
    return execute_query(query=query, close_con=True)


def get_AllUsers():
    query = """SELECT * FROM user"""
    return execute_query(query=query, close_con=False, data="all")


def get_UserById(user_id): 
    query = """SELECT * FROM user
            WHERE ID = {}""".format(user_id)
    return execute_query(query=query, close_con=False, data="one")

def get_UserByUsername(username):
    query = """SELECT * FROM user 
            WHERE Username = '{}'""".format(username)
    return execute_query(query=query, close_con=False, data="one")

def get_AllUserTransactions(user_id):
    query = """SELECT * FROM transaction 
            WHERE User_id = {}""".format(user_id)
    return execute_query(query=query, close_con=False, data="all")

def get_AllUserTransactionsByUsername(username):

    user = get_UserByUsername(username)

    query = """SELECT * FROM transaction 
            WHERE User_id = '{}'""".format(user['ID'])
    return execute_query(query=query, close_con=False, data="all")

def get_BasicInfoByUsername(username):
    query = """SELECT Username, Password FROM user 
            WHERE Username = '{}'""".format(username)
    return execute_query(query=query, close_con=False, data="one")


def get_BalanceByUsername(username):
    query = """SELECT ID, Username, Balance FROM user 
            WHERE Username = '{}'""".format(username)
    return execute_query(query=query, close_con=False, data="one")


def update_UserInfo(data):
    query = """UPDATE user 
            SET 
            Username = '{}', 
            Password = '{}' 
            WHERE ID = {}""".format(data["username"], data["password"],
                                    data["id"])
    return execute_query(query=query, close_con=True)


def update_UserBalance(data):
    query = """UPDATE user 
            SET 
            Balance = {} 
            WHERE ID = {}""".format(data["balance"], data["id"])
    return execute_query(query=query, close_con=True)


def delete_UserById(id):
    query = """DELETE FROM user
            WHERE ID = {}""".format(id)
    return execute_query(query=query, close_con=True)


def delete_UserTransaction(data):
    query = """DELETE FROM transaction 
            WHERE User_id = {} AND ID = {}""".format(data["user_id"], data["id"])
    return execute_query(query=query, close_con=True)


def IsAdmin(username):
    query = """SELECT IsAdmin FROM user 
            WHERE Username = '{}'""".format(username)
    return execute_query(query=query, close_con=False, data="one")


def open_db_connection():
    connection = db_connector()
    cursor = connection.cursor(dictionary=True)
    return connection, cursor


def commit_and_close_db_connection(connection, cursor):
    connection.commit()
    cursor.close()
    connection.close()