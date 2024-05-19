from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutUser, name="logout"),
    path('', views.home, name='home'),
    path('product-detail/<str:pk>', views.product_detail, name='product-detail'),
    path('create-product/', views.create_product, name="create-product"),
    path('edit-product/<str:pk>', views.edit_product, name="edit-product"),
    path('delete-product/<str:pk>/', views.delete_product, name="delete-product"),
    path('sugar-calc/', views.sugar_calc, name='sugar-calc'),
    path('imt-calc/', views.imt_calc, name='imt-calc'),
    path('products/', views.products, name='products'),
    path('user-profile/', views.profile, name='user-profile'),
    path('update-profile/', views.update_profile, name='update-profile'),
]