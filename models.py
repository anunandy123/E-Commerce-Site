from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.
class Customer(models.Model):
    name=models.CharField(max_length=30,blank=True,null=True)
    email=models.EmailField()
    password=models.CharField(max_length=40)
    address=models.TextField()
    phonenumer=models.CharField(max_length=10)
    def __str__(self):
        return self.name
class Category(models.Model):
    name=models.CharField(max_length=100,unique=True)
    def __str__(self):
        return self.name
    
class Products(models.Model):
    PRODUCTS_SIZE=[
        ('S','Small'),
        ('M','Medium'),
        ('L','Learge'),
        ('XL','Extra Learge'),
    ]
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name="products")
    name=models.CharField(max_length=40)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    sdesc=models.CharField(max_length=200)
    ldesc=models.TextField()
    quatity=models.IntegerField()
    color=models.CharField(max_length=20)
    size=models.CharField(max_length=2,choices=PRODUCTS_SIZE)
    image=models.ImageField(upload_to="dresses/",blank=True,null=True)
    review=models.IntegerField(null=True,blank=True)
    brand=models.CharField(max_length=50,blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
          
    