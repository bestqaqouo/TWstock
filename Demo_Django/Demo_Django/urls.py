"""Demo_Django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from TWStockChart.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index),#首頁
    path('make_image/',make_image),#製作圖表頁面
    path('searching/',searching),#快速查詢頁面
    # path('twstock_search/',stock_search),
    path('result/',result),#快速查詢結果頁面
    path('get_image/',get_image),#圖表輸出頁面
]
