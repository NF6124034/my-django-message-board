from django.urls import path
from .views import hello

urlpatterns = [
    path('hello/<str:name>', hello),  # ✅ 當用戶訪問 /hello/，會執行 hello() 這個 View
]
