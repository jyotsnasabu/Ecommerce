
from django.urls import path,include
from . import views
urlpatterns = [
    path('index',views.index,name="index"),
    path('login',views.login,name="login"),
    path('signup',views.signup,name="signup"),
    path('signup1',views.signup1,name="signup1"),
    path('login1',views.login1,name="login1"),
    path('admin_page',views.admin_page,name="admin_page"),
    path('addcategory',views.addcategory,name="addcategory"),
    path('addcategory1',views.addcategory1,name="addcategory1"),
    path('addproduct',views.addproduct,name="addproduct"),
    path('addproduct1',views.addproduct1,name="addproduct1"),
    path('product_list', views.product_list, name='product_list'),
    path('products/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    path('confirm_delete', views.confirm_delete, name='confirm_delete'),
    path('user_details', views.user_details, name='user_details'),
    path('user-details/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    path('category_page/<int:category_id>/', views.category_page, name='category_page'),
    path('cart_page',views.cart_page,name="cart_page"),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_cart/<int:cart_item_id>/',views.update_cart, name='update_cart'),
    path('remove_from_cart/<int:cart_item_id>/',views.remove_from_cart, name='remove_from_cart'),
     path('checkout',views.checkout,name="checkout"),
     path('success',views.success,name="success"),
     path('logout',views.logout,name="logout"),
     path('',views.home,name="home"),
]

