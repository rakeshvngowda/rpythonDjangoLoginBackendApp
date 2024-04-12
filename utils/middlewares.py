from utils.jsonWebToken import verifyToken
from utils.CustomError import CustomError
from django.http import JsonResponse
from django.core.cache import cache


def authVerify(func):
    def inner(request):
        try:
            autherization = request.headers['Authorization']
            verifyToken(autherization)
            return func(request)
        except Exception as e:
            message = getattr(e,'args','')[0]
            return JsonResponse({'message':'Invalid Autherization'},status=500)
    return inner


def storeApiData(func):
    def inner(request):
        try:
            cached_data = cache.get('usersList')
            if cached_data:
                return JsonResponse({"status":200,"data":cached_data},status=200)
            return func(request)
        except Exception as e:
            message = getattr(e,'args','')[0]
            return JsonResponse({'message':'Invalid Autherization'},status=500)
    return inner