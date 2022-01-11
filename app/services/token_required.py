import config
from flask import request, jsonify
import jwt
from functools import wraps
from app.services.db_helper import IsAdmin

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None
        if 'authorization' in request.headers:
            token = request.headers['authorization']
        if not token:
            return jsonify({'message': 'a valid token is missing'})
        
        data = jwt.decode(token, config.SECRET_KEY, algorithms=["HS256"])
        
        is_admin = IsAdmin(data["username"])

        if is_admin["IsAdmin"] == 0:
            return "You are not autherized"

        return f(*args, **kwargs)
    return decorator


def Usertoken_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None
        if 'authorization' in request.headers:
            token = request.headers['authorization']
        if not token:
            return jsonify({'message': 'a valid token is missing'})
        
        data = jwt.decode(token, config.SECRET_KEY, algorithms=["HS256"])
        
        current_user = data['username']

        return f(current_user, *args, **kwargs)
    return decorator