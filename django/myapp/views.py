from django.shortcuts import render,redirect
from . models import Contact,User,Product,Wishlist,Cart
from django.core.exceptions import ObjectDoesNotExist
import random
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.
def index(request):
	try:
		user=User.objects.get(email=request.session['email_id'])
		if user.usertype=='buyer':
			return render(request,'index.html')
		else:
			return render(request,'seller-index.html')
	except:
		return render(request,'index.html')


	


def contact(request):
	if request.method=='POST':
		Contact.objects.create(
			name=request.POST['name'],
			email=request.POST['email'],
			mobile=request.POST['mobile'],
			message=request.POST['m_sgs']
			)
		msg='Contact saved successfully'
		return render(request,'contact.html',{'msg':msg})
		
	else:
		return render(request,'contact.html')


def signup(request):
	if request.method=='POST':
		try:

			user=User.objects.get(email=request.POST['email'])
			msg='User already registered'
			return render(request,'login.html',{'msg':msg})

		except:
			User.objects.create(
				usertype=request.POST['cat'],
				fname=request.POST['fname'],
				lname=request.POST['lname'],
				email=request.POST['email'],
				mobile=request.POST['mobile'],
				address=request.POST['address'],
				password=request.POST['password'],
				profile_pic=request.FILES['profile_picture']
				)
			msg='User registered successfully'
			return render(request,'login.html',{'msg':msg})
	else:
		return render(request,'signup.html')


def login(request):
	if request.method=='POST':
		try:
			user=User.objects.get(email=request.POST['email_id'])
			if user.password==request.POST['password']:
				request.session['fname']=user.fname
				request.session['email_id']=user.email
				request.session['profile_picture']=user.profile_pic.url
				request.session['usertype']=user.usertype
				wishlists=Wishlist.objects.filter(user=user)
				request.session['wishlist_count']=len(wishlists)
				carts=Cart.objects.filter(user=user,payment_status=False)
				request.session['cart_count']=len(carts)
				msg='User logged in successfully'
				if user.usertype=='buyer':
					return render(request,'index.html',{'msg':msg})
				else:
					return render(request,'seller-index.html',{'msg':msg})
				
			else:
				msg='Password Incorrect'
				return render(request,'login.html',{'msg':msg})
		except ObjectDoesNotExist:
			msg='User not registered'
			return render(request,'signup.html',{'msg':msg})
	else:
		return render(request,'login.html')


def logout(request):
	try:
		del request.session['email_id']
		del request.session['fname']
		del request.session['profile_picture']
		del request.session['usertype']
		msg='User logged out successfully'
		return render(request,'login.html')
	except:
		msg='User logged out successfully'
		return render(request,'login.html')


def change_password(request):
	user=User.objects.get(email=request.session['email_id'])
	
	if request.method=='POST':			
		if user.password==request.POST['old_password']:
			if user.password!=request.POST['new_password']:
				if request.POST['new_password']==request.POST['cnew_password']:
					user.password=request.POST['new_password']
					user.save()
					del request.session['email_id']
					del request.session['fname']
					msg='Password Updated successfully'
					return render(request,'login.html',{'msg':msg})
				else:
					msg='New Password ad confirm new password does not match'
					if user.usertype=='buyer':
						return render(request,'change-password.html',{'msg':msg})
					else:
						return render(request,'seller-change-password.html',{'msg':msg})
			else:
				msg='New password can not be old passwords'
				if user.usertype=='buyer':
					return render(request,'change-password.html',{'msg':msg})
				else:
					return render(request,'seller-change-password.html',{'msg':msg})
		
		else:
			msg='Password Incorrect'
			if user.usertype=='buyer':
				return render(request,'change-password.html',{'msg':msg})
			else:
				return render(request,'seller-change-password.html',{'msg':msg})
		
	else:
		if user.usertype=='buyer':
			return render(request,'change-password.html')
		else:
			return render(request,'seller-change-password.html')
		


def forgot_password(request):
	if request.method=='POST':
		try:
			user=User.objects.get(email=request.POST['email_id'])
			otp=str(random.randint(1000,9999))
			subject='OTP For Forgot Password'
			message="Hello"+user.fname+'Your OTP for Forgot Password is'+str(otp)
			email_from=settings.EMAIL_HOST_USER
			recipient_list=[user.email,]
			send_mail( subject, message, email_from, recipient_list )
			request.session['email_id']=user.email
			request.session['otp']=otp
			return render(request,'otp.html')
		except User.DoesNotExist:
			msg='User not found'
			return render(request,'signup.html',{'msg':msg})
	else:
		return render(request,'forgot-password.html')


def verify_otp(request):
	if request.method=='POST':
		otp1=int(request.POST['otp'])
		otp2=int(request.session['otp'])
		if otp1==otp2:
			del request.session['otp']
			return render(request,'new-password.html')
		else:
			msg='Incorrect OTP'
			return render(request,'otp.html',{'msg':msg})
	else:
			return render(request,'otp.html')

def new_password(request):
	if request.POST['n_password']==request.POST['c_password']:
		user=User.objects.get(email=request.session['email_id'])
		if user.password!=request.POST['n_password']:
			user.password=request.POST['n_password']
			user.save()
			del request.session['email_id']
			msg='Password Updated successfully'
			return render(request,'login.html',{'msg':msg})
		else:
			msg='New password cannot be same as old password'
			return render(request,'new-password.html',{'msg':msg})
	else:
		msg='New Password and confirm New Password does not match'
		return render(request,'new-password.html',{'msg':msg})

def profile(request):
	user=User.objects.get(email=request.session['email_id'])
	if request.method=='POST':
		user.usertype=request.POST['usertype']
		user.fname=request.POST['fname']
		user.lname=request.POST['lname']
		user.address=request.POST['address']
		user.mobile=request.POST['mobile']
		try:
			user.profile_pic=request.FILES['profile_picture']
		except:
			pass
		user.save()
		request.session['profile_picture']=user.profile_pic.url
		msg='Profile Updated successfully'
		if user.usertype == 'buyer':
			return render(request,'profile.html',{'msg':msg,'user':user})
		else:
			return render(request,'seller-profile.html',{'msg':msg,'user':user})
	else:
		if user.usertype == 'buyer':
			return render(request,'profile.html',{'user':user})
		else:
			return render(request,'seller-profile.html',{'user':user})


def seller_add_product(request):
	seller=User.objects.get(email=request.session['email_id'])
	if request.method=='POST':
		Product.objects.create(
			seller=seller,
			product_category=request.POST['category'],
			product_name=request.POST['product_name'],
			product_desc=request.POST['product_desc'],
			product_price=request.POST['product_price'],
			product_image=request.FILES['product_image']
			
			)
		msg='Product Added Successfully'
		return render(request,'seller-add-product.html',{'msg':msg})
	else:
		return render(request,'seller-add-product.html')

def seller_view_product(request):
	seller=User.objects.get(email=request.session['email_id'])
	products=Product.objects.filter(seller=seller)
	return render(request,'seller-view-product.html',{'products':products})

def seller_product_detail(request,pk):
	product=Product.objects.get(pk=pk)
	return render(request,'seller-product-detail.html',{'product':product})

def seller_product_edit(request,pk):
	product=Product.objects.get(pk=pk)
	if request.method=='POST':
		product.product_category=request.POST['category']
		product.product_name=request.POST['product_name']
		product.product_desc=request.POST['product_desc']
		product.product_price=request.POST['product_price']
		try:
			product.product_image=request.FILES['product_image']
		except:
			pass
		product.save()
		msg='Product Updated successfully'
		return render (request,'seller-product-edit.html',{'msg':msg,'product':product})

	else:
		return render (request,'seller-product-edit.html',{'product':product})

def seller_product_delete(request,pk):
	product=Product.objects.get(pk=pk)
	product.delete()
	msg='Product deleted successfully'
	return redirect('seller-view-product')

def buyer_product_detail(request,pk):
	product=Product.objects.get(pk=pk)
	return render(request,'buyer-product-detail.html',{'product':product})

def products(request):
	products=Product.objects.all()
	return render(request,'products.html',{'products':products})

def add_to_wishlist(request,pk):
	user=User.objects.get(email=request.session['email_id'])
	product=Product.objects.get(pk=pk)
	Wishlist.objects.create(
		user=user,
		product=product
		)
	return redirect('wishlist')

def wishlist(request):
	user=User.objects.get(email=request.session['email_id'])
	wishlists=Wishlist.objects.filter(user=user)
	request.session['wishlist_count']=len(wishlists)
	return render(request,'wishlist.html',{'wishlists':wishlists})

def remove_from_wishlist(request,pk):
	user=User.objects.get(email=request.session['email_id'])
	product=Product.objects.get(pk=pk)
	wishlist=Wishlist.objects.get(user=user,product=product)
	wishlist.delete()
	return redirect('wishlist')


def products_by_cat(request,cat):
	products=Product()
	if cat == 'all':
		products=Product.objects.all()
	else:
		products=Product.objects.filter(product_category=cat)
	return render(request,'products.html',{'products':products})

def add_to_cart(request,pk):
	user=User.objects.get(email=request.session['email_id'])
	product=Product.objects.get(pk=pk)
	Cart.objects.create(
		user=user,
		product=product,
		product_price=product.product_price,
		product_qty=1,
		total_price=product.product_price,
		payment_status=False
		)
	return redirect('cart')


def cart(request):
	net_price=0
	user=User.objects.get(email=request.session['email_id'])
	carts=Cart.objects.filter(user=user,payment_status=False)
	request.session['cart_count']=len(carts)

	for i in carts:
		net_price=net_price+i.total_price
	return render(request,'cart.html',{'carts':carts,'net_price': net_price})

def remove_from_cart(request,pk):
	user=User.objects.get(email=request.session['email_id'])
	product=Product.objects.get(pk=pk)
	cart=Cart.objects.get(user=user,product=product)
	cart.delete()
	return redirect('cart')

def change_qty(request):
	product_qty=int(request.POST['product_qty'])
	cid=int(request.POST['cid'])
	cart=Cart.objects.get(pk=cid)
	cart.product_qty=product_qty
	cart.total_price=cart.product_price*product_qty
	cart.save()
	return redirect('cart')