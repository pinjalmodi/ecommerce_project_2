from django.db import models
from django.utils import timezone

# Create your models here.
class Contact(models.Model):
	name=models.CharField(max_length=100)
	email=models.EmailField()
	mobile=models.PositiveIntegerField()
	message=models.TextField()

	def __str__(self):
		return self.name



class User(models.Model):
	usertype=models.CharField(max_length=100, choices=[
		('seller','seller'),
		('buyer','buyer')
		],
		)
	fname=models.CharField(max_length=100)
	lname=models.CharField(max_length=100)
	email=models.EmailField()
	mobile=models.PositiveIntegerField()
	address=models.TextField()
	password=models.CharField(max_length=100)
	profile_pic=models.ImageField(upload_to='profile_pic/',default='')

	def __str__(self):
		return self.fname+'-'+self.usertype


class Product(models.Model):
	cat=(
		('Men','Men'),
		('Women','Women'),
		('Kids','Kids')
		)
	seller=models.ForeignKey(User,on_delete=models.CASCADE)
	product_name=models.CharField(max_length=100)
	product_desc=models.TextField()
	product_category=models.CharField(max_length=100,choices=cat)
	product_price=models.PositiveIntegerField()
	product_image=models.ImageField(upload_to='product_image/',default='')

	def __str__(self):
		return self.seller.fname+'-'+self.product_name


class Wishlist(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	product=models.ForeignKey(Product,on_delete=models.CASCADE)
	date=models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.user.fname+'-'+self.product.product_name

class Cart(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	product=models.ForeignKey(Product,on_delete=models.CASCADE)
	date=models.DateTimeField(default=timezone.now)
	product_price=models.PositiveIntegerField()
	product_qty=models.PositiveIntegerField()
	total_price=models.PositiveIntegerField()
	payment_status=models.BooleanField(default=False)

	def __str__(self):
		return self.user.fname+' - '+self.product.product_name