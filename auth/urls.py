from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('redis/',views.redisApiCaching,name='redis'),
    path('order/',views.order,name='order'),
]