from django.urls import path
from . import views

urlpatterns = [
    path('index/',views.index,name='index'),
    path('seller-index/', views.index, name='seller-index'),
    path('contact/',views.contact,name='contact'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('change-password/',views.change_password,name='change-password'),
    path('forgot-password/',views.forgot_password,name='forgot-password'),
    path('verify-otp/',views.verify_otp,name='verify-otp'),
    path('new-password/',views.new_password,name='new-password'),
    path('profile/',views.profile,name='profile'),
    path('seller-add-product/',views.seller_add_product,name='seller-add-product'),
    path('seller-view-product/',views.seller_view_product,name='seller-view-product'),
    path('seller-product-detail/<int:pk>/',views.seller_product_detail,name='seller-product-detail'),
    path('seller-product-edit/<int:pk>/',views.seller_product_edit,name='seller-product-edit'),
    path('seller-product-delete/<int:pk>/',views.seller_product_delete,name='seller-product-delete'),
    path('buyer-product-detail/<int:pk>/',views.buyer_product_detail,name='buyer-product-detail'),
    path('products/',views.products,name='products'),
    path('add-to-wishlist/<int:pk>',views.add_to_wishlist,name='add-to-wishlist'),
    path('wishlist/',views.wishlist,name='wishlist'),
    path('remove-from-wishlist/<int:pk>/',views.remove_from_wishlist,name='remove-from-wishlist'),
    path('products-by-cat/<str:cat>/',views.products_by_cat,name='products-by-cat'),
    path('add-to-cart/<int:pk>',views.add_to_cart,name='add-to-cart'),
    path('cart/',views.cart,name='cart'),
    path('remove-from-cart/<int:pk>',views.remove_from_cart,name='remove-from-cart'),
    path('change-qty/',views.change_qty,name='change-qty'),




]