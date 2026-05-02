from django.db import models
from django.utils.safestring import mark_safe
# Create your models here.

class RegisterModel(models.Model):
    name = models.CharField(max_length=25)
    email = models.EmailField()
    phone = models.IntegerField()
    password = models.CharField(max_length=16)
    address = models.TextField()
    dp = models.ImageField(upload_to="photos")
    gender = models.CharField(max_length=10)
    role = models.CharField(max_length=10)

    def __str__(self):
        return self.name


    def image(self):
        return mark_safe('<img src={} width="100px">'.format(self.dp.url))

class category(models.Model):
    catname=models.CharField(max_length=25)

    def __str__(self):
        return self.catname

class color(models.Model):
    colorname=models.CharField(max_length=25)
    colorcode=models.CharField(max_length=10)

    def __str__(self):
        return self.colorcode

class product(models.Model):
    pname=models.CharField(max_length=30)
    catid=models.ForeignKey(category,on_delete=models.CASCADE)
    pimg=models.ImageField(upload_to="photos")
    price=models.FloatField()
    description=models.TextField()
    status=models.CharField(max_length=15,default='available')
    sellerid=models.ForeignKey(RegisterModel,on_delete=models.CASCADE)
    color = models.ManyToManyField(color, blank=True)

    def __str__(self):
        return self.pname

    def product_img(self):
        return mark_safe('<img src={} width="100px">'.format(self.pimg.url))

class Cart(models.Model):
    userid=models.ForeignKey(RegisterModel,on_delete=models.CASCADE)
    productid=models.ForeignKey(product,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    totalprice=models.FloatField()
    orderstatus=models.IntegerField()
    orderid=models.IntegerField()

class Order(models.Model):
    userid = models.ForeignKey(RegisterModel,on_delete=models.CASCADE)
    finaltotal = models.FloatField()
    phone = models.CharField(max_length=10)
    address = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField()
    paymode = models.CharField(max_length=10)
    razorpay_orderid = models.CharField(max_length=35,blank=True,null=True)


class Wishlist(models.Model):
    userid = models.ForeignKey(RegisterModel,on_delete=models.CASCADE)
    productid = models.ForeignKey(product,on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)













