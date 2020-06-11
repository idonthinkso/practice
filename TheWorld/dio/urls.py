from django.urls import path

from dio import views

app_name = 'dio'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('getdetail/', views.getdetail, name='getdetail'),
    path('show_booklist/', views.show_booklist, name='show_booklist'),
    path('getcaptcha/', views.getcaptcha, name='getcaptcha'),
    path('checkname/', views.check_name, name='checkname'),
    path('checkcapt/', views.checkcapt, name='checkcapt'),
    path('register/', views.register, name='register'),
    path('registerlogic/', views.registerlogic, name='registerlogic'),
    path('registerok/', views.registerok, name='registerok'),
    path('checkpwd/', views.checkpwd, name='checkpwd'),
    path('login/', views.login, name='login'),
    path('loginlogic/', views.loginlogic, name='loginlogic'),
    path('addbook/', views.addbook, name='addbook'),
    path('cart/', views.show_cart, name='cart'),
    path('remove_car_item/', views.remove_car_item, name='remove_car_item'),
    path('del_car_item/', views.del_car_item, name='del_car_item'),
    path('add_car_item/', views.add_car_item, name='add_car_item'),
    path('address/', views.address, name='address'),
    path('queryaddress/', views.queryaddress, name='queryaddress'),
    path('orderlogic/', views.order_logic, name='orderlogic'),
    path('delsession/', views.delsession, name='delsession'),
    path('pro/', views.pro, name='pro'),
    path('checkcart/', views.checkcart, name='checkcart'),
]
