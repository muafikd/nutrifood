from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import OuterRef, Subquery
from .utils import *


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, "Такого пользователя не существует")
        
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Неправильная почта или пароль")
    context = {'page':page}
    return render(request, 'app/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = MyUserCreationForm()

    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Ошибка во время регистрации. Проверьте все поля на корректность')
    return render(request, 'app/login_register.html', {'form' : form })

# @login_required(login_url='login')
def home(request):
    return render(request, 'app/home.html')

def products(request):
    # Subquery to fetch the main photo for each product
    main_photo_subquery = ProductPhoto.objects.filter(product=OuterRef('pk')).order_by('id').values('photo')[:1]

    # Query to fetch products along with their main photos
    products_with_photos = Product.objects.annotate(main_photo=Subquery(main_photo_subquery))

    context = {'products': products_with_photos}
    return render(request, 'app/products.html', context)

def sugar_calc(request):
    context = {'calc': 'sugar'}

    if request.method == 'POST':
        age = int(request.POST.get('age', 0))
        gender = request.POST.get('gender', 'male')  # По умолчанию мужской
        height = int(request.POST.get('height', 170))  # Средний рост, если не указан
        weight = int(request.POST.get('weight', 70))  # Средний вес, если не указан
        activity_level = request.POST.get('activity', 'low')  # Низкий уровень активности по умолчанию

        calories = calculate_calories_based_on_age(gender, age, height, weight, activity_level)
        sugar_grams_10 = calculate_sugar_intake(calories, 10)
        sugar_grams_5 = calculate_sugar_intake(calories, 5)

        context['result'] = f'10% сахара: {sugar_grams_10:.2f} грамм, 5% сахара: {sugar_grams_5:.2f} грамм'
    return render(request, 'app/calc.html', context)

def imt_calc(request):
    context = {'calc' : 'imt'}
    if request.method == 'POST':
        weight = float(request.POST.get('weight'))
        height = float(request.POST.get('height')) / 100  # Преобразуем см в метры
        bmi = weight / (height ** 2)
        context['bmi_result'] =f'{bmi:.2f}'
    return render(request, 'app/calc.html', context)

# @login_required(login_url='login')
def product_detail(request, pk):
    product = Product.objects.get(id=pk)
    product_photos = ProductPhoto.objects.filter(product=product)
    context = {'product': product, 'product_photos': product_photos}
    return render(request, 'app/product-detail.html', context)


@login_required
def create_product(request):
    if not request.user.is_superuser:
        return redirect('home')
    
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()

            # Handle product photos
            photos = request.FILES.getlist('photos')
            for photo in photos:
                ProductPhoto.objects.create(product=product, photo=photo)

            # messages.success(request, 'Продукт создан успешно!')
            return redirect('home')
    else:
        form = ProductForm()  # No need to pass existing_photos
    context = {'form': form}
    return render(request, 'app/product-form.html', context)


@login_required
def edit_product(request, pk):
    if not request.user.is_superuser:
        return redirect('home')
    
    product = Product.objects.get(id=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()

            # Handle photo deletion
            for key, value in form.cleaned_data.items():
                if key.startswith('photo_') and value:
                    photo_id = int(key.split('_')[1])
                    ProductPhoto.objects.filter(id=photo_id).delete()

            # Handle new photos
            new_photos = request.FILES.getlist('photos')
            for photo in new_photos:
                ProductPhoto.objects.create(product=product, photo=photo)

            # messages.success(request, 'Продукт обновлен успешно!')
            return redirect('home')
    else:
        form = ProductForm(instance=product)
    context = {'form': form, 'product': product}
    return render(request, 'app/product-form.html', context)

@login_required
def delete_product(request, pk):
    if not request.user.is_superuser:
        return redirect('home')
    product = Product.objects.get(id=pk)
    # if request.user != room.host:
    #     return HttpResponse('You are not allowed!')
    if request.method == "POST":
        product.delete()
        return redirect('products')
    return render(request, 'app/delete.html', {'obj' : product})

@login_required
def profile(request):
    user = request.user
    context = {
        'user': user
    }
    return render(request, 'app/user-profile.html', context)

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user-profile')  # Перенаправление на страницу профиля после обновления
    else:
        form = UpdateProfileForm(instance=request.user)
    return render(request, 'app/update-profile.html', {'form': form})