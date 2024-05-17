from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Category
from .models import Product,Cart



def home(request):
    categories = Category.objects.all() 
    
    return render(request,'home.html',{'categories': categories})


def index(request):
    categories = Category.objects.all() 
    cart_items = Cart.objects.filter(user=request.user)
    cart_items_count = cart_items.count()
    return render(request,'index.html',{'categories': categories,'cart_items_count': cart_items_count})


def login(request):
    categories = Category.objects.all() 
    return render(request,'login.html',{'categories': categories})


def signup(request):
    categories = Category.objects.all() 
    return render(request,'signup.html')


from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import userdetails

def signup1(request):
    if request.method == 'POST':
       
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')
        address = request.POST.get('address')
        contact = request.POST.get('contact')
        email = request.POST.get('email')
        photo = request.FILES.get('photo')

        
        if password != confirm_password:
            messages.info(request,'Password not mathching')
            return render(request, 'signup.html', )

      
        user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, email=email)


        user_detail = userdetails.objects.create(user=user, address=address, number=contact, img=photo)
        user_detail.save()
    
        

        return redirect('login')
    return render(request, 'signup.html')

def login1(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            if user.is_superuser:
                auth.login(request,user)
                return redirect('admin_page')
            
            else:
                auth.login(request,user)
                messages.info(request,f'Welcome {username}')
                return redirect('index')
        else:
            messages.info(request,'Invalid username or password ,try again')
            return redirect('login1')
    else:
        return redirect('login1')
    


def admin_page(request):
    return render(request,'admin_page.html')


def addcategory(request):
    return render(request,'addcategory.html')


def addcategory1(request):
    if request.method == 'POST':
        category_name = request.POST.get('category')
        category = Category.objects.create(category_name=category_name)
        category.save()
        return redirect('admin_page')  
    return render(request, 'add_category.html')

def addproduct(request):
    categories = Category.objects.all()  # Retrieve all categories
    return render(request, 'addproduct.html', {'categories': categories})


def addproduct1(request):
    if request.method == 'POST':
        try:
            # Retrieve form data from POST request
            pname = request.POST.get('productName')
            pdesc = request.POST.get('description')
            pprice = request.POST.get('price')
            pimg = request.FILES.get('file')
            category_id = request.POST.get('category')
            
            # Retrieve category instance
            category = Category.objects.get(id=category_id)
            
            # Create new product instance and save to database
            product = Product(pname=pname, pdesc=pdesc, pprice=pprice, pimg=pimg, category=category)
            product.save()
            # Redirect to admin home page
            return redirect('admin_page')  # Replace 'admin_home' with your actual URL name for the admin home page
        except Exception as e:
            print(e)  # Print any exceptions that occur
            return redirect('admin_page')  # Redirect to admin home page or handle the error gracefully
    else:
        # Retrieve all categories to populate category dropdown
        categories = Category.objects.all()
        return render(request, 'addproduct.html', {'categories': categories})



def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})


def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'confirm_delete.html', {'product': product})


def confirm_delete(request):
    return render(request,'confirm_delete.html')




def user_details(request):
    users = userdetails.objects.all()
    return render(request, 'user_details.html', {'users': users})



def delete_user(request, user_id):
    user = get_object_or_404(userdetails, pk=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('user_details')
    return render(request, 'confirm_delete.html', {'user': user})




def category_page(request, category_id):
    category = Category.objects.get(pk=category_id)
    products = Product.objects.filter(category=category)
    categories = Category.objects.all() 
    return render(request, 'category_page.html', {'category': category, 'products': products,'categories': categories})


def cart_page(request):
    cart_items = Cart.objects.filter(user=request.user)  # Assuming user is logged in
    total_price = sum(item.total_price() for item in cart_items)
    categories = Category.objects.all() 
    return render(request, 'cart_page.html', {'cart_items': cart_items, 'total_price': total_price, 'categories': categories})



from django.shortcuts import redirect, get_object_or_404
from .models import Product, Cart


def add_to_cart(request, product_id):
    # Retrieve the product object
    product = get_object_or_404(Product, pk=product_id)
    
    if request.method == 'POST':
        # Create or update the cart item
        cart_item, created = Cart.objects.get_or_create(user=request.user, prod=product)
        if not created:
            cart_item.quantity += 1  # Increment quantity if the product is already in the cart
        cart_item.save()
        
        # Redirect the user to the cart page
        return redirect('cart_page')
    
    # Redirect to the index page if the request method is not POST
    return redirect('index')


def remove_from_cart(request, cart_item_id):
    # Retrieve the cart item object
    cart_item = get_object_or_404(Cart, pk=cart_item_id)
    
    if request.method == 'POST':
        # Delete the cart item
        cart_item.delete()
        
        # Redirect the user to the cart page
        return redirect('cart_page')
    
    # Redirect to the index page if the request method is not POST
    return redirect('index')



from django.http import HttpResponseRedirect
from django.urls import reverse

from django.http import HttpResponseRedirect
from django.urls import reverse

def update_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, pk=cart_item_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        quantity = int(request.POST.get('quantity'))
        if action == 'subtract':
            cart_item.quantity -= 1 if cart_item.quantity > 1 else 0
        elif action == 'add':
            cart_item.quantity += 1
        cart_item.save()
        return HttpResponseRedirect(reverse('cart_page'))
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, pk=cart_item_id)
    if request.method == 'POST':
        cart_item.delete()
        return HttpResponseRedirect(reverse('cart_page'))
    


def checkout(request):

    return render(request,'checkout.html')



def success(request):
    
    return render(request,'success.html')


def logout(request):
    auth.logout(request)
    return redirect('home')

