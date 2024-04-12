import jwt
import os
from datetime import datetime,timedelta
from django.http import JsonResponse
from utils.CustomError import CustomError
SECRET = os.getenv('JWT_SECRET')

def createToken(username):
    try:
        payload = {"username": username,'exp':datetime.utcnow()+timedelta(minutes=30)} # Expiry time 30 minutes from now
        token = jwt.encode(payload, SECRET, algorithm='HS256')
        return token
    except Exception as e:
        message = getattr(e,'messages','') or getattr(e,'args','')
        raise CustomError(message)

def verifyToken(token):
    try:
        return jwt.decode(token, SECRET, algorithms='HS256')
    except Exception as e:
        message = getattr(e,'args','')[0]
        raise CustomError(message)

    
