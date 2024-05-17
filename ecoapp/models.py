from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class userdetails(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    address=models.CharField(max_length=255)
    number=models.CharField(max_length=255)
    img=models.ImageField(upload_to="images/",null=True)



class Category(models.Model):
    category_name=models.CharField(max_length=255)


class Product(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    pname=models.CharField(max_length=255)
    pprice=models.IntegerField()
    pdesc=models.CharField(max_length=255)
    pimg=models.ImageField(upload_to="images/",null=True)
class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    prod=models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    quantity=models.IntegerField(default=1)
    def total_price(self):
        return self.quantity*self.prod.pprice