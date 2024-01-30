
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth import logout,authenticate,login
from django.contrib.auth.models import User,AbstractUser
from django.contrib.auth import get_user_model
from django.urls import reverse
from app.models import Cart, Product,Customer,Order
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum



# Create your views here.
def home(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'app/home.html', context)


@login_required(login_url="/login")
def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        user = request.user

        existing_cart_item = Cart.objects.filter(user=user, product_id=product).first()

        if existing_cart_item:
            existing_cart_item.quantity += quantity
            existing_cart_item.save()
        else:
            Cart.objects.create(user=user, product_id=product, quantity=quantity)

        # Calculate the total quantity of items in the cart
        total_quantity = Cart.objects.filter(user=user).aggregate(Sum('quantity'))['quantity__sum']

        # Update the session with the total quantity
        request.session['total_quantity'] = total_quantity

        return redirect('home')

    return render(request, 'app/home.html', {'product': product})


def signin(request):
    if request.method == 'GET':
        return render(request,'app/login.html')
    else:
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You are now logged in.')
            next_url=request.GET.get('next')
            if next_url :
                return redirect(next_url)
            
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')  
       
def register(request):
    if request.method == 'GET':
        return render(request, 'app/register.html')
    else:
        fn = request.POST['firstname']
        ln = request.POST['lastname']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']

        User = get_user_model()

        # Use create_user method from the custom user model manager
        user = User.objects.create_user(first_name=fn, last_name=ln, email=email, username=username, password=password)

        return redirect('home')

def Signout(request):
    Cart.objects.filter(user=request.user).delete()
    logout(request)
    return redirect('home')



def cartbox(request):
    cart_items = Cart.objects.filter(user=request.user)

    return render(request, 'app/cartbox.html', {'cart_items': cart_items})



@login_required(login_url="/login")
def delete(request, id):
    try:
        add_to_cart = get_object_or_404(Cart, id=id)
    
    # Update session quantity by subtracting the quantity of the deleted item
        request.session['quantity'] = max(0, request.session.get('quantity', 0) - add_to_cart.quantity)
    
        add_to_cart.delete()
    except:
        return render(request,'app/error.html',{'msg':'Items does not exits'})
    
    return redirect('cartbox')




def edit(request, id):
    cart = Cart.objects.get(id=id)

    if request.method == 'POST':
        new_quantity = request.POST.get('quantity')

        # Validate that the new quantity is a positive integer
        if not new_quantity.isdigit() or int(new_quantity) <= 0:
            error_message = "Please enter a valid positive quantity."
            return render(request, 'app/edit.html', {'cart': cart, 'error_message': error_message})

        # Update the cart quantity and save
        cart.quantity = int(new_quantity)
        cart.save()

        return redirect('cartbox')

    return render(request, 'app/edit.html', {'cart': cart})
    
    




def order(request):
    user_cart = Cart.objects.filter(user=request.user)

    # Create an order for each item in the cart
    orders = []
    for cart_item in user_cart:
        order = Order.objects.create(
            user=request.user,
            cart=cart_item,
            product=cart_item.product_id,  # Access the product through the Cart model
        )
        orders.append(order)

        # Optionally, you can update the inventory or perform other actions

    # Clear the user's cart after creating orders
    user_cart.delete()

    # Calculate the total price for all orders
    total_price = sum(order.total_price() for order in orders)

    return render(request, 'app/order.html', {'orders': orders, 'total_price': total_price})
