from django.db import models

# Create your models here.

class Post(models.Model):#資料庫建立與管理
    company_name = models.CharField(max_length=100)
    capacity = models.CharField(max_length=100)
    turnover = models.CharField(max_length=100)
    open = models.CharField(max_length=100)
    high = models.CharField(max_length=100)
    low = models.CharField(max_length=100)
    close = models.CharField(max_length=100)
    transactions = models.CharField(max_length=100)
    change = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    def __str__(self):
        return self.company_name