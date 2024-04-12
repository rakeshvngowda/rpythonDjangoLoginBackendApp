from django.shortcuts import render
from django.http import JsonResponse
from utils.CustomError import CustomError
from django.db import connection
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
import json
import bcrypt
from utils.passwordHash import hashPassword, verifyPassword
from utils.dbConnection import DbConnection
from utils.passwordHash import hashPassword, verifyPassword
from utils.jsonWebToken import createToken, verifyToken
from utils.middlewares import authVerify,storeApiData
from django.core.cache import cache
import jwt
import requests
db = DbConnection()


# Create your views here.
@authVerify
@storeApiData
def index(request):
    response = db.exceuteRequest('GET_USERS')
    cache.set('usersList',response)
    return JsonResponse({"status": 200, "data": response, }, status=200)


def signup(request):
    try:
        if (request.method == 'POST'):
            body = json.loads(request.body)
            username = body["username"]
            password = hashPassword(body["password"]).decode('utf-8')
            validate_password(password)
            validate_email(username)
            query = "ADD_USER"
            params = (username, password)
            response = db.exceuteRequest(query, params)
            token = createToken(username)
            return JsonResponse({"user":username,"token": token})
        else:
            # return JsonResponse({"msg":"login page"})
            raise CustomError("APi Not found")
    except Exception as error:
        message = getattr(error, 'message', '') or getattr(error, 'messages', '')
        return JsonResponse({'msg': message}, status=500)


def login(request):
    try:
        if (request.method != 'POST'):
            raise CustomError("Method Not found")
        body = json.loads(request.body)
        username = body["username"]
        password = body["password"]
        query = "GET_SINGLE_USER"
        params = (username,)
        result = db.exceuteRequest(query,params)
        verifyPassword(password,result[0][2])
        token = createToken(username)
        return JsonResponse({"username":username,"token":token},status=200)
    except Exception as error:
        message = getattr(error,'message','') or getattr(error,'messages','')
        return JsonResponse({'msg':message},status=500)

@authVerify
def redisApiCaching(request):
    cached_data = cache.get('users')
    
    if (cached_data):
        cached_data = json.loads(cached_data)
        return JsonResponse(cached_data)
    response =requests.get('https://reqres.in/api/users?page=2')
    
    data = response.json()
    cache.set('users',json.dumps(data),timeout=30)
    return JsonResponse(data)

@authVerify
def order(request):
    try:
        if (request.method == 'GET'):
            query = 'SELECT * FROM GET_ORDERS'
            response = db.exceuteView(query)
            return JsonResponse({"data":response})
        return JsonResponse(json.loads(request.body))
    except Exception as error:
        message = getattr(error,'message','') or getattr(error,'messages','')
        return JsonResponse({'msg':message},status=500)

