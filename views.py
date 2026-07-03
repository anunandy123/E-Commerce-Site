from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from .models import Customer,Category,Products
from django.contrib import messages

# Create your views here.
def Home(request):
    return render(request,"Home.html")
def Product(request):
    categories = Category.objects.all()
    category_id = request.GET.get('category')

    if category_id:
        products = Products.objects.filter(category_id=category_id)
    else:
        products = Products.objects.all()
    context = {
        'categories': categories,
        'products': products
    }
    return render(request, "Product.html", context)  
def product_detail(request, id):
    product = get_object_or_404(Products, id=id)
    return render(request, 'product_detail.html', {'product': product}) 
def cart(request):
    if not request.session.get('user_id'):
        return redirect('login-page')

    cart = request.session.get('cart')

    if not cart:
        return render(request, 'cart.html', {
            'cart_items': [],
            'total': 0
        })

    product_ids = list(map(int, cart.keys()))
    products = Products.objects.filter(id__in=product_ids)

    cart_items = []
    total = 0

    for product in products:
        qty = cart.get(str(product.id), 0)
        subtotal = product.price * qty
        total += subtotal

        cart_items.append({
            'product': product,
            'quantity': qty,
            'subtotal': subtotal
        })

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })


def add_to_cart(request, id):
    if not request.session.get('user_id'):
        return redirect('login-page')

    cart = request.session.get('cart', {})

    if str(id) in cart:
        cart[str(id)] += 1
    else:
        cart[str(id)] = 1

    request.session['cart'] = cart

    # 🔥 Redirect back to product detail page
    return redirect('product_detail', id=id)

def remove_from_cart(request, id):
    cart = request.session.get('cart', {})
    cart.pop(str(id), None)
    request.session['cart'] = cart
    return redirect('cart')
def About(request):
    return render(request,"about.html")
def Contact(request):
    return render(request,"Contact.html")
def Signup(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        address = request.POST.get("address")
        password = request.POST.get("password")
        phonenumer = request.POST.get("phonenumer")

        if Customer.objects.filter(email=email).exists():
            messages.error(request, "User already exists")
            return redirect("signup-page")

        Customer.objects.create(
            name=name,
            email=email,
            password=password,
            address=address,
            phonenumer=phonenumer
        )

        messages.success(request, "Registration successful")
        return redirect("login-page")

    return render(request, "Signup.html")

def Login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = Customer.objects.get(email=email, password=password)
            request.session['user_id'] = user.id
            request.session['user_name'] = user.name
            request.session['user_email'] = user.email

            messages.success(request, "Login successful")
            return redirect("home-page")

        except Customer.DoesNotExist:
            messages.error(request, "Invalid email or password")

    return render(request, "login.html")
def Logout(request):
    request.session.flush()   # clears all session data
    messages.success(request, "Logged out successfully")
    return redirect("login-page")
def checkout(request):
    if not request.session.get('user_id'):
        return redirect('login-page')

    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "Your cart is empty")
        return redirect('cart')

    total = 0
    products = Products.objects.filter(id__in=cart.keys())

    for product in products:
        total += product.price * cart[str(product.id)]

    return render(request, 'checkout.html', {'total': total})
def payment_success(request):
    if request.method == "POST":
        request.session.pop('cart', None)  # clear cart
        messages.success(request, "Payment successful! Order placed.")
        return redirect('home-page')

