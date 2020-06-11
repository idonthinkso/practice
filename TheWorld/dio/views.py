import hashlib
import json
import os
import random
import string
from itertools import chain

from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from dio.captcha.image import ImageCaptcha
from dio.cart import Cart, Cart_Item
from dio.models import TBookType, TBookDetails, TUser, TCart, TUserAddress


def index(request):
    one_category =TBookType.objects.filter(super__isnull=True)
    # print(one_category)
    two_category = TBookType.objects.filter(super__isnull=False)
    # print(two_category)
    books = TBookDetails.objects.all().order_by('-publication_date')[:8]
    # print(books)
    hotbooks = TBookDetails.objects.all().order_by('-score')[:8]
    newfire = TBookDetails.objects.all().order_by('score', '-publication_date')[:10]

    username = request.session.get('username')
    # username = request.COOKIES.get('username')

    return render(request,'dio/home.html',{'username': username,
                                                   'one_category': one_category,
                                                   'two_category': two_category,
                                                   'books': books,
                                                   'hotbooks': hotbooks,
                                                    'newfire': newfire})


def getdetail(request):
    id = request.GET.get('id')
    book = TBookDetails.objects.get(id=id)
    # book.book_type --> TBookType object (21)
    # 获取二级标题名

    two_name = book.book_type.type_name
    # 获取一级标题id
    one_id = book.book_type.super_id
    # 获取一级标题名
    one = TBookType.objects.get(id=one_id)
    one_name = one.type_name

    # username = request.COOKIES.get('username')
    username = request.session.get('username')
    return render(request,'dio/Book details.html',{'one_cage_name':one_name,
                                                           'two_cage_name':two_name,
                                                           'book':book,
                                                           'username':username})


def show_booklist(request):
    one_category = TBookType.objects.filter(super__isnull=True)
    two_category = TBookType.objects.filter(super__isnull=False)
    num = request.GET.get('page')
    if num is None:
        num = 1
    category_id = request.GET.get('category_id')
    # 将分类id存入session
    if category_id is not None:
        request.session['category_id'] = category_id
    else:
        category_id = request.session.get('category_id')
    print(category_id)
    sort = request.GET.get('sort')


    print(sort)

    category = TBookType.objects.get(id=category_id)
    username = request.session.get('username')
    # 如果点一级分类
    if not category.super_id:
        #     需要将一级分类的名字传给模板---one_category
        # o_category_id = category.id
        o_category_name = category.type_name  # 一级分类的名字
        t_category_name = None
        # 要先找出一级分类下的所有的二级分类
        two_categorys = TBookType.objects.filter(super__id=category_id)
        two_categorys_ids = [i.id for i in two_categorys]
        qsets = []
        for two_id in two_categorys_ids:
            qsets.append(TBookDetails.objects.filter(book_type__id=two_id))
        if qsets:
            books = qsets[0]
            for i in range(1, len(qsets)):
                books = books | qsets[i]
            print(type(books))
            if sort == '0':
                books = books
            elif sort == '1':
                books = books.order_by('-comment')
                print(books)
            elif sort == '2':
                books = books.order_by('price')
            else:
                books = books.order_by('-publication_date')

            pg = Paginator(books, per_page=3)
            pg1 = pg.page(num)
        else:
            books = []
            pg = Paginator(books, per_page=3)
            pg1 = pg.page(num)
    else:
        # 如果点二级分类
        o_category_name = TBookType.objects.get(id=category.super_id).type_name  # 一级分类的名字
        # o_category_id = category.super_id
        t_category_name = category.type_name
        # t_category_id= category.id
        # 根据分类直接获取二级分类所对应的书籍
        # 0:默认排序  1:销量降序  2：价格升序  3.出版时间降序
        if sort == '0':
            books = TBookDetails.objects.filter(book_type=category_id)
        elif sort == '1':
            books = TBookDetails.objects.filter(book_type=category_id).order_by('-comment')
            print(books)
        elif sort == '2':
            books = TBookDetails.objects.filter(book_type=category_id).order_by('price')
        else:
            books = TBookDetails.objects.filter(book_type=category_id).order_by('-publication_date')
        # books = TBookDetails.objects.filter(book_type__id=category_id)

        pg = Paginator(books, per_page=3)
        pg1 = pg.page(num)
        # print(pg.count)

    return render(request, 'dio/booklist.html', {'one_category': one_category,
                                                         'two_category': two_category,
                                                         'page': pg1,
                                                         'ca_id': category_id,
                                                         'o_category_name': o_category_name,
                                                         't_category_name': t_category_name,
                                                         'username':username,
                                                            'sort':sort
                                                            })


# 生成验证码
def getcaptcha(request):
    img = ImageCaptcha()
    code = random.sample(string.ascii_letters + string.digits, 4)
    random_code = ''.join(code)
    print(random_code)
    request.session['code']=random_code
    captcha = img.generate(random_code)
    return HttpResponse(captcha,'image/jpg')


# 核对用户名
def check_name(request):
    username = request.POST.get('username')
    rst = TUser.objects.filter(username=username)
    if rst:
        return HttpResponse('0')
    return HttpResponse('1')


# 核对验证码
def checkcapt(request):
    code = request.POST.get('code')
    if code.lower() == request.session['code'].lower():
        return HttpResponse('1')
    return HttpResponse('0')


# 注册入口
def register(request):
    form = request.GET.get('form')
    return render(request,'dio/register.html', {'form': form})


# 生成随机字符串
def getRandstr(n):
    str = ''.join(random.sample(string.ascii_letters + string.digits, n))
    return str


# 处理注册表单传来的数据
def registerlogic(request):
    try:
        with transaction.atomic():
            form = request.GET.get('form', '')
            username = request.POST.get('txt_username')
            pwd = request.POST.get('txt_password')
            # 对密码进行加密
            # 每个用户的每一个密码都要使用独一无二的盐值
            salt = getRandstr(10)
            # 对密码进行加密
            q = (pwd + salt).encode()
            h = hashlib.sha256(q)
            secreted_pwd = h.hexdigest()
            print(secreted_pwd)
            # 保存用户名---保持登录名
            request.session['username'] = username
            rst = TUser.objects.create(username=username, password=secreted_pwd, salt=salt)
            if not form:
                rsp = render(request, 'dio/register ok.html', {'username': username,
                                                                       'form': form})
            rsp = render(request, 'dio/register ok.html', {'username': username,
                                                                   'form': form})
            if rst:
                # 默认7天免登陆---设置cookie
                # , max_age=7 * 24 * 60 * 60
                rsp.set_cookie('username', username, max_age=7*24*60*60)
                rsp.set_cookie('pwd', secreted_pwd, max_age=7*24*60*60)
            return rsp
    except:
        return HttpResponse('哎呀')


def registerok(request):
    form = request.GET.get('form')
    username = request.session.get('username')
    return render(request,'dio/register ok.html',{'form':form,
                                                          'username': username})


def checkpwd(request):
    username = request.POST.get('username')
    pwd = request.POST.get('pwd')
    rst = TUser.objects.filter(username=username).first()
    # 与数据库中加密过的密码比对，是否一致
    salt = rst.salt
    password = rst.password
    se_pwd = hashlib.sha256((pwd + salt).encode()).hexdigest()
    if se_pwd == password:
        return HttpResponse('1')
    return HttpResponse('0')


def login(request):
    username = request.COOKIES.get('username')
    pwd = request.COOKIES.get('pwd')  # cookie中存储的是加密过的密码
    if request.session.get('login') == 'ok':
        if 'cart/' in request.META.get('HTTP_REFERER', ''):
            cart = request.session.get('cart')
            username = request.session.get('username')
            return render(request, 'dio/address.html', {'username': username,
                                                                'cart': cart})
    rst = TUser.objects.filter(username=username, password=pwd)
    form = request.GET.get('form')
    request.session['from'] = form
    if rst:
        request.session['login'] = 'ok'
        request.session['username'] = username
        return redirect('dio:index')
    return render(request, 'dio/login.html')


def loginlogic(request):
    username = request.POST.get('txtUsername')
    pwd = request.POST.get('txtPassword')
    rst = TUser.objects.filter(username=username).first()
    # 与数据库中加密过的密码比对，是否一致
    salt = rst.salt
    password = rst.password
    se_pwd = hashlib.sha256((pwd + salt).encode()).hexdigest()
    if se_pwd != password:
        return render(request, 'dio/400.html')
    request.session['username'] = username
    # 是否需要七天免登陆
    remember = request.POST.get('autologin')
    form = request.session.get('from')
    print(form)
    # 设置session，存储用户名，保持登录状态
    request.session['login'] = 'ok'
    # 加载购物车---获取该用户的id
    user_id = TUser.objects.filter(username=username).first().id
    # 查询该用户的购物车
    user_cart = TCart.objects.filter(user_id=user_id)
    # 看看是否有cart这个session
    cart = request.session.get('cart')
    # 如果有，说明在未登录状态下，购物车有该用户添加的商品
    if cart:
        # 查询该用户在数据库中的购物车，对比，如果有商品，将商品进行更新
        for i in user_cart:
            for car_item in cart.car_items:
                if car_item.book.id == i.book_id:
                    # 更改数据库中书对应的数量
                    col = TCart.objects.get(user_id=user_id, book_id=i.book_id)
                    col.number += car_item.num
                    col.save()
                else:
                    # 如果数据库中没有该书，将他存入数据库中
                    TCart.objects.create(user_id=user_id, book_id=car_item.book.id, number=car_item.num)
    # 创建一个新的购物车对象，用来存放该用户购物车中的所有东西---登陆和未登录状态下的所有的商品
    cart = Cart()
    # 从数据库中取出该用户的购物车
    for i in TCart.objects.filter(user_id=user_id):
        cart.add_item(i.book_id, i.number)
    request.session['cart'] = cart
    # 如果是从购物车页面调过来的，应该调到订单地址页面
    if form == 'cart':
        rsp = render(request, 'dio/address.html', {'username': username,
                                                           'cart': cart})
        if remember:
            rsp.set_cookie('username', username, max_age=7*24*60*60)
            rsp.set_cookie('pwd', se_pwd, max_age=7*24*60*60)
        return rsp
    # 其他地方均跳回首页
    rsp = redirect('dio:index')
    # 7天自动登录，设置cookie
    # ,max_age=7*24*60*60
    if remember:
        rsp.set_cookie('username', username, max_age=7*24*60*60)
        rsp.set_cookie('pwd', se_pwd, max_age=7*24*60*60)
    return rsp


def addbook(request):
    book_id = request.POST.get('book_id')
    book_num = request.POST.get('book_num')

    # book_id = request.GET.get('book_id')
    # book_num = request.GET.get('book_num')

    if request.session.get('cart') is None:
        cart = Cart()
    else:
        cart = request.session.get('cart')
    # # 获取购物车中商品的总数
    # sum = 0

    if book_id and book_num:
        # 判断传过来的数字是否合法
        for i in book_num:
            if not i.isdecimal():
                return render(request, 'dio/400.html')
        cart.add_item(int(book_id), int(book_num))

    # for i in cart.car_items:
    #     sum += i.num
    request.session['cart'] = cart

    return HttpResponse('ok')


def show_cart(request):
    username = request.session.get('username')
    cart = request.session.get('cart')
    # 获取购物车中商品的总数
    sum = 0
    if cart:
        for i in cart.car_items:
            sum += i.num

    return render(request,'dio/cart.html', {'username': username,
                                                    'cart': cart,
                                                    'sum': sum})


def del_car_item(request):
    # 数量减一
    book_id = request.POST.get('book_id')
    cart = request.session.get('cart')
    cart.modify(int(book_id), 1)
    request.session['cart'] = cart
    username = request.session.get('username')
    if username:
        #     说明登陆了
        user_id = TUser.objects.get(username=username).id
        TCart.objects.filter(user_id=user_id, book_id=book_id).update(number=F('number') - 1)
        # cart_info = TCart.objects.get(user_id=user_id, book_id=book_id)
        # cart_info.number -= 1
        # cart_info.save()
    return HttpResponse('1')


def add_car_item(request):
    # 数量加一
    book_id = request.POST.get('book_id')
    cart = request.session.get('cart')
    cart.add_item(int(book_id))
    request.session['cart'] = cart
    username = request.session.get('username')
    if username:
        # 说明登陆了
        user_id = TUser.objects.get(username=username).id
        TCart.objects.filter(user_id=user_id, book_id=book_id).update(number=F('number')+1)
    return HttpResponse('1')


def remove_car_item(request):
    book_id = request.POST.get('book_id')
    num = request.POST.get('num')
    print(id)
    cart = request.session.get('cart')
    cart.del_item(int(book_id))
    request.session['cart'] = cart
    username = request.session.get('username')
    if username:
        # 说明登陆了
        user_id = TUser.objects.get(username=username).id
        TCart.objects.filter(user_id=user_id, book_id=book_id).delete()
    return HttpResponse('1')


def address(request):
    try:

        username = request.session.get('username')
        cart = request.session.get('cart')
        sum = 0
        for i in cart.car_items:
            sum += i.num
        return render(request,'dio/address.html',{'username': username,
                                                          'cart': cart,
                                                          'sum': sum})
    except:
        return render(request, 'dio/400.html')


def defaultfn(a):
    if isinstance(a, TUserAddress):
        return {
            'id':a.id,
            'detail':a.detail,
            'zipcode':a.zipcode,
            'name':a.name,
            'phone':a.phone,
            'fixphone':a.fixphone
        }


def queryaddress(request):
    username =request.POST.get('username')
#     查出该用户id
    user_id = TUser.objects.filter(username=username).first().id
#     关联地址表---查询出该用户的历史地址
    add_info = TUserAddress.objects.filter(user_id=user_id)
#     将该用户对应的地址信息传给前端
    if add_info:
        # 如果有历史地址
        rst = json.dumps(list(add_info), default=defaultfn)
        return HttpResponse(rst)
    return HttpResponse('0')


def randomcode(n):
    return ''.join(random.sample(string.digits, n))


def order_logic(request):
    # del request.session['cart']
    cart = Cart()
    request.session['cart'] = cart
    print(request.session.get('cart'))
    # 支付金额---商品数量---收货人

    price = request.GET.get('price')
    num = request.GET.get('num')
    add_id = request.GET.get('addid')
    order_info = request.POST.getlist('ship_man')
    username = request.session.get('username')
    # 随机生成一个订单号---8位
    order_code = randomcode(8)

    user_id = TUser.objects.filter(username=username).first().id
    print(order_info)
    # if order_info:
    # # 将数据添加到数据库中
    #     TUserAddress.objects.create()
    rst = TUserAddress.objects.filter(user_id=user_id, id=add_id).first()
    if rst:
        if not order_info:
           return render(request, 'dio/indent ok.html', {'person':rst.name,
                                                          'num':num,
                                                          'price':price,
                                                          'username':username,
                                                          'order_code':order_code})
    TUserAddress.objects.create(detail=order_info[1],
                                zipcode=order_info[2],
                                name=order_info[0],
                                user_id=user_id,
                                phone=order_info[3],
                                fixphone=order_info[4])
    return render(request, 'dio/indent ok.html', {'person':order_info[0],
                                                          'num':num,
                                                          'price':price,
                                                          'username':username,
                                                          'order_code':order_code})


def delsession(request):
    # del request.session['cart']
    # del request.session['username']
    # del request.session['login']
    request.session.flush()  # 清除数据，置空cookie中的sessionid，清除数据表中的记录

    return redirect('dio:index')


def pro(request):
    return render(request,'dio/pro.html')


def checkcart(request):
    cart = request.session.get('cart')
    # print(cart.car_items)
    if cart.car_items == []:
        # print('@@@@@')
        return HttpResponse('0')
    return HttpResponse('1')

