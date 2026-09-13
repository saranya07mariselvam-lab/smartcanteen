from django.shortcuts import render , redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .models import Food, Order



def home(request):
    foods = Food.objects.filter(available=True)
    return render(request, 'home.html', {'foods': foods})

def order_food(request, food_id):
    food = Food.objects.get(id=food_id)

def order_list(request):
    orders = Order.objects.all().order_by('-id')
    return render(request, 'order_list.html', {'orders': orders})

    if request.method == 'POST':
        quantity = int(request.POST['quantity'])
        if quantity > food.stock:
         return render(request, 'order.html', {
        'food': food,
        'error': 'Not enough stock available!'
    })
        total_price = food.price * quantity

        food.stock = food.stock - quantity
        food.save()

        order = Order.objects.create(
    food=food,
    quantity=quantity,
    total_price=total_price
)

        return render (request, 'success.html', {'order': order})

    return render(request, 'order.html', {'food': food})

def add_to_cart(request, food_id):
    cart = request.session.get('cart', {})

    food_id = str(food_id)

    if food_id in cart:
        cart[food_id] += 1
    else:
        cart[food_id] = 1

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')

def cart(request):
    cart = request.session.get('cart', {})

    foods = []
    total = 0

    for food_id, quantity in cart.items():
        food = Food.objects.get(id=food_id)

        item_total = food.price * quantity
        total += item_total

        foods.append({
            'food': food,
            'quantity': quantity,
            'item_total': item_total
        })

    return render(request, 'cart.html', {
        'foods': foods,
        'total': total
    })

def increase_cart(request, food_id):
    cart = request.session.get('cart', {})

    food_id = str(food_id)

    if food_id in cart:
        cart[food_id] += 1

    request.session['cart'] = cart

    return redirect('cart')

def decrease_cart(request, food_id):
    cart = request.session.get('cart', {})

    food_id = str(food_id)

    if food_id in cart:
        cart[food_id] -= 1

        if cart[food_id] <= 0:
            del cart[food_id]

    request.session['cart'] = cart

    return redirect('cart')

def place_cart_order(request):
    cart = request.session.get('cart', {})

    if not cart:
        return render(request, 'cart.html', {
            'foods': [],
            'total': 0
        })

    total = 0

    for food_id, quantity in cart.items():
        food = Food.objects.get(id=food_id)

        # Check stock
        if quantity > food.stock:
            return render(request, 'cart.html', {
                'foods': [],
                'total': 0,
                'error': f'Not enough stock for {food.name}'
            })

        total += food.price * quantity

    # Create separate Order entries for each food
    orders = []

    for food_id, quantity in cart.items():
        food = Food.objects.get(id=food_id)

        item_total = food.price * quantity

        order = Order.objects.create(
            food=food,
            quantity=quantity,
            total_price=item_total
        )

        # Reduce stock
        food.stock = food.stock - quantity
        food.save()

        orders.append(order)

    # Clear cart
    request.session['cart'] = {}

    return render(request, 'cart_success.html', {
        'orders': orders,
        'total': total
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

        return render(request, 'login.html', {
            'error': 'Invalid username or password'
        })

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        from django.contrib.auth.models import User

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {
                'error': 'Username already exists'
            })

        User.objects.create_user(
            username=username,
            password=password
        )

        return redirect('login')

    return render(request, 'register.html')

def my_orders(request):
    orders = Order.objects.all().order_by('-id')

    return render(request, 'my_orders.html', {
        'orders': orders
    })