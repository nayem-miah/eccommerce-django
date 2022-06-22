from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
import random
from django_countries.fields import CountryField


ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

class Categories(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, null=True, blank=True)
  
    def __str__(self):
        return self.name


class Filter_Price(models.Model):
    FILTER_PRICE =(
        ('1000 To 10000', '1000 To 10000'),
        ('2000 To 20000', '2000 To 20000'),
        ('3000 To 30000', '3000 To 30000'),
        ('4000 To 40000', '4000 To 40000'),
        ('5000 To 50000', '5000 To 50000'),
    )

    price = models.CharField(choices=FILTER_PRICE, max_length=60)

    def __str__(self):
        return self.price


class User_Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Product(models.Model):
    CONDITION = (('New','New'),('Old','Old'))
    STOCK = ('IN STOCK','IN STOCK'),('OUT OF STOCK','OUT OF STOCK')
    STATUS = ('Publish','Publish'),('Draft','Draft')

    unique_id = models.CharField(unique=True, max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='Product_images/img')
    name = models.CharField(max_length=200)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    condition = models.CharField(choices=CONDITION, max_length=100)
    information = models.CharField(max_length=300)
    description = RichTextField(null=True)
    stock = models.CharField(choices=STOCK, max_length=200)
    status = models.CharField(choices=STATUS, max_length=200)
    created_date = models.DateTimeField(default=timezone.now)

    categories = models.ForeignKey(Categories,on_delete=models.CASCADE,null=True, blank=True)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE,null=True, blank=True)
    color = models.ForeignKey(Color,on_delete=models.CASCADE,null=True, blank=True)
    filter_price = models.ForeignKey(Filter_Price,on_delete=models.CASCADE,null=True, blank=True)




    def save(self, *args, **kwargs):
    

            ran = "".join(random.choice(['1','d','3','x','4','5','r','7','y', 't','d','o']) for x in range(12))

            self.unique_id = ran
            return super().save(*args,**kwargs)




    def __str__(self):
        return self.name



class Card(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        name_quantity = f"{self.quantity}piece of {self.product.name}"
        return name_quantity

    def total_product_price(self):
       return self.quantity * self.product.price

    
    def discount(self):
        if self.product.discount_price:
            return self.product.discount_price
        return 0


    def total_discount_price(self):
        if self.product.discount_price:
          return self.quantity * self.product.discount_price
        return 0
 

    def final_total_money(self):
        if self.product.discount_price:
          price = self.total_product_price() - self.total_discount_price()
          return price
        return self.total_product_price()



class Order_Item(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)


    def __str__(self):
        name_quantity = f"{self.quantity}piece of {self.product.name}"
        return name_quantity

    def total_product_price(self):
       return self.quantity * self.product.price

    
    def discount(self):
        if self.product.discount_price:
            return self.product.discount_price
        return 0


    def total_discount_price(self):
        if self.product.discount_price:
          return self.quantity * self.product.discount_price
        return 0
 

    def final_total_money(self):
        if self.product.discount_price:
          price = self.total_product_price() - self.total_discount_price()
          return price
        return self.total_product_price()






class Order(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    order_item = models.ManyToManyField(Order_Item)
    address = models.ForeignKey('Address', on_delete=models.CASCADE, related_name='buy_address',blank=True, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    ordered = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)


    def __str__(self):
        return self.user.username


    def get_total(self):
        a = 0
        for d in self.order_item.all():
            a+=d.final_total_money()
        return a

     


class Address(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    city = models.CharField(max_length=100, null=True, blank=True)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    

    def __str__(self):
        return self.user.username


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
