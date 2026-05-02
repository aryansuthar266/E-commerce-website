from django.contrib import messages
from django.db.models import *
from django.shortcuts import render , redirect
from django.utils.translation.trans_real import catalog
import razorpay
from p1 import settings

from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
# Create your views here.

def register(request):
    return render(request, 'register.html')

def registerdata(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        address = request.POST.get('address')
        dp = request.FILES['dp']
        gender = request.POST.get('gender')
        role = request.POST.get('role')

        print(name,email,phone,password,address,dp,gender,role)
# insert query
        insertquery = RegisterModel(name=name, email=email,phone=phone,password=password,address=address,dp=dp,gender=gender,role=role)
        insertquery.save()
        messages.success(request, 'Registered Successfully')
        return render(request, 'register.html')
    return render(request, 'register.html')

def login(request):
    return render(request, 'login.html')

def logindata(request):
    if request.method == "POST":
        uemail = request.POST.get('uemail')
        upassword = request.POST.get('upassword')

        try:
            userdata = RegisterModel.objects.get(email=uemail, password=upassword)

            request.session["log_id"] = userdata.id
            request.session["log_name"] = userdata.name
            request.session["log_email"] = userdata.email
            request.session["log_role"] = userdata.role
            print("login success")
            messages.success(request, 'Login Successful')
            return redirect("/")

        except RegisterModel.DoesNotExist:
            print("login fail")
            messages.error(request, 'Invalid Email or Password')
            return redirect("/login")

    return render(request, 'login.html')

def logout(request):
    try:
        del(request.session["log_id"])
        del(request.session["log_name"])
        del(request.session["log_email"])
        del(request.session["log_role"])
        print("logout success")
        return redirect("/logindata")
    except:
        pass
    return render(request, 'showproduct.html')

def show(request):
    cat=category.objects.all()
    pro=product.objects.all()
    context = {
        'category':cat,
        'data':pro,
    }
    return render(request, 'showproduct.html',context)

def addpro(request):
    catagory=category.objects.all()
    context = {
        'catagory':catagory,
    }
    return render(request, 'addpro.html',context)

def insertpro(request):
    if request.method == "POST":
        name = request.POST.get('name')
        catid = request.POST.get('catid')
        pimg = request.FILES['pimg']
        price = request.POST.get('price')
        description = request.POST.get('description')
        status = request.POST.get('status')
        sellerid = request.session.get('log_id')

        insertquery = product(pname=name,catid=category(id=catid),pimg=pimg,price=price,
                              description=description,status=status,sellerid=RegisterModel(id=sellerid))
        insertquery.save()
        messages.success(request, 'Product Added Successfully')
        return redirect("/")
    return render(request, 'addpro.html')

def singleproduct(request,id):
    product1 = product.objects.get(id=id)
    col = color.objects.all()
    context = {
        'product':product1,
        'color':col,
    }
    return render(request, 'singleproduct.html',context)

def catvisepro(request,id):
    cat = category.objects.all()
    pro = product.objects.filter(catid=id)
    context = {
        'category':cat,
        'product':pro,
    }
    return render(request, 'catvisepro.html',context)

def exclude(request):
    cat = category.objects.all()
    data = product.objects.exclude(status="unavailable")
    context = {
        'cat':cat,
        'data':data,
    }
    return render(request, 'exclude.html',context)


def sort(request):
    Category = category.objects.all()
    sort = request.GET.get("sort", "price")
    Product = product.objects.all().order_by(sort)

    allowed_sort_fields = ['pname', '-pname', 'price', '-price']

    if sort in allowed_sort_fields:
        sort = 'name'
    elif sort == 'price':
        sort = 'price'


    context = {
        "category": Category,
        "sort": sort,
        "data": Product,

    }
    return render(request, "sort.html", context)

def showcount(request):
    cat = category.objects.all()
    t_pro = product.objects.count()
    avail_pro = product.objects.filter(status__iexact="available").count()
    unavail_pro = product.objects.filter(status__iexact="unavailable").count()
    t_user = RegisterModel.objects.filter(role="user").count()
    t_seller = RegisterModel.objects.filter(role="Seller").count()
    pro = product.objects.all()
    context = {
        'cat':cat,
        't_pro':t_pro,
        'avail_pro':avail_pro,
        'unavail_pro':unavail_pro,
        't_user':t_user,
        't_seller':t_seller,
        'pro':pro,
    }
    return render(request, 'showcount.html',context)

def showvalues(request):
    cat = category.objects.all()
    pro = product.objects.values('id','pname','price','status')
    context = {
        'cat':cat,
        'pro':pro,
    }
    return render(request, 'showvalues.html',context)

def aggregation(request):
    Category = category.objects.all()
    Product = product.objects.all()
    stats = product.objects.aggregate(
        total_products = Count("id"),
        average_price = Avg("price"),
        highest_price = Max("price"),
        lowest_price = Min("price"),
        total_values = Sum("price"),
    )
    context = {
        "category": Category,
        "product": Product,
        "stats" : stats,
    }
    return render(request, "aggregate.html",context)

def showselectrelated(request):
    Category = category.objects.all()
    Product = product.objects.select_related("catid","sellerid").all()
    context = {
        "category":Category,
        "product":Product
    }
    return render(request,"sel_related.html",context)

def showcolor(request):
    cat = category.objects.all()
    pro = product.objects.prefetch_related("color").all()
    col = color.objects.all()
    context = {
        "cat":cat,
        "pro":pro,
        "color":col,
    }
    return render(request,"showcolor.html",context)

def singleproductnew(request,id):
    Category = category.objects.all()
    Product = product.objects.get(id=id)
    Color = color.objects.all()
    context = {
        "category":Category,
        "product":Product,
        "color":Color
    }
    return render(request,"showsinglecolor.html",context)


def insertcart(request):
    if request.method == "POST":
        userid = request.session["log_id"]
        productid = request.POST.get("productid")
        quantity = int(request.POST.get("quantity"))
        amount = float(request.POST.get("amount"))

        fetchdata = Cart.objects.filter(userid=RegisterModel(id=userid), productid=product(id=productid),
                                        orderstatus=1).first()

        if fetchdata:
            fetchdata.quantity += quantity
            fetchdata.totalprice = fetchdata.quantity * amount
            fetchdata.save()
        else:

            Cart.objects.create(userid=RegisterModel(id=userid), productid=product(id=productid), quantity=quantity,
                                totalprice=quantity * amount, orderstatus=1, orderid=0)

        messages.success(request, "Product added to cart")
        return redirect("/")

    return render(request, "singleproduct.html")

def cart(request):
    userid = request.session["log_id"]
    data = Cart.objects.filter(userid=RegisterModel(id=userid),orderstatus=1)
    total = (sum(i.totalprice for i in data))
    context = {
        "data":data,
        "total":total,
    }
    return render(request,"cart.html",context)

def deletecart(request,id):
    userid = request.session['log_id']
    Cart.objects.get(id=id).delete()
    return redirect(cart)

def increase(request, id):
    data = Cart.objects.get(id=id)
    data.quantity += 1
    data.totalprice += data.productid.price
    data.save()
    return redirect("/cart")

def decrease(request,id):
    fetchdata = Cart.objects.get(id=id)
    if fetchdata.quantity == 1:
        fetchdata.delete()
        messages.success(request,"Product Removed from Cart")
        return redirect("/")
    else:
        fetchdata.quantity -= 1
        fetchdata.totalprice -= fetchdata.productid.price
        fetchdata.save()
        return redirect(cart)

def manageproduct(request):
    sellerid = request.session["log_id"]
    Category = category.objects.all()
    Product = product.objects.filter(sellerid=RegisterModel(id=sellerid))
    context = {
        "category":Category,
        "Product":Product,

    }

    return render(request,"manageproduct.html",context)

def deleteproduct(request,id):
    product.objects.get(id=id).delete()
    messages.success(request,"Product Deleted")
    return redirect("/manageproduct")

def editproduct(request,id):
    Category = category.objects.all()
    Product = product.objects.get(id=id)
    context = {
        "category":Category,
        "product":Product,
    }
    return render(request,"editproduct.html",context)

def updatedata(request):
    if request.method == "POST":
        productid = request.POST.get("productid")
        productname = request.POST.get("productname")
        catid = request.POST.get("catid")
        price = request.POST.get("price")
        description = request.POST.get("description")
        status = request.POST.get("status")

        productdetails = product.objects.get(id=productid)
        productdetails.pname = productname
        productdetails.catid.catname = category(id=catid)
        productdetails.price = price
        productdetails.description = description
        productdetails.status = status

        if "pimg" in request.FILES:
            productdetails.pimg = request.FILES["pimg"]
            productdetails.save()
        productdetails.save()
        return redirect("/manageproduct")
    return render(request,"editproduct.html")

def placeorder(request):
    userid = request.session["log_id"]
    finaltotal = request.POST.get("finaltotal")
    phone = request.POST.get("phone")
    address = request.POST.get("address")
    paymode = request.POST.get("paymode")

    if paymode == "Cash on Delivery":
        storedata = Order(userid=RegisterModel(id=userid), finaltotal=finaltotal, phone=phone, address=address, status=True, paymode=paymode)
        storedata.save()
        messages.success(request, "Order Place Successfully")

        #order id
        lastid = storedata.id

        #update cart
        cart = Cart.objects.filter(userid=RegisterModel(id=userid), orderstatus=1)

        for i in cart:
            i.orderid=lastid
            i.orderstatus=0
            i.save()

        print("Cart Updated")

        return redirect("/")

    else:
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))
        order_amount = int(float(finaltotal) * 100)  # Razorpay needs amount in paise

        razorpay_order = client.order.create({
            "amount": order_amount,
            "currency": "INR",
            "receipt": f"order_rcptid_{userid}",
            "payment_capture": "1",
        })

        storedata = Order(
            userid=RegisterModel(id=userid), finaltotal=finaltotal, phone=phone, address=address, status=True,
            paymode="Online", razorpay_orderid=razorpay_order['id'])
        storedata.save()

        lastid = storedata.id

        # Update Cart Items
        cart = Cart.objects.filter(userid=userid, orderstatus=1)
        for i in cart:
            i.status = 0
            i.orderid = lastid
            i.save()

        return render(request, "payment.html", {
            "razorpay_order_id": razorpay_order['id'],
            "amount": order_amount,
            "key": settings.RAZORPAY_KEY_ID,
            "currency": "INR",
        })

def payment_success(request):
    return redirect("/")

def myorder(request):
    userid = request.session["log_id"]
    order = Order.objects.filter(userid=RegisterModel(id=userid))

    order_details = []
    for o in order:
        items = Cart.objects.filter(orderid=o.id)
        order_details.append({
            "order":o,
            "items":items,
        })
    context = {
        "order_details":order_details,

    }
    return render(request,"myorder.html",context)

def sellerorders(request):
    sellerid = request.session["log_id"]
    seller_products = product.objects.filter(sellerid=RegisterModel(id=sellerid))
    seller_product_ids = seller_products.values_list('id',flat=True)
    cart_items = Cart.objects.filter(productid__in = seller_product_ids, orderstatus = 0)
    context = {
        "items":cart_items
    }

    return render(request,"sellerorder.html",context)


def addwishlist(request,id):
    login_id = request.session["log_id"]

    if Wishlist.objects.filter(productid=id).exists():
        messages.success(request,"This Item already present in wishlist")
        return redirect("/showproduct")

    Product = product.objects.get(id=id)
    user = RegisterModel.objects.get(id = login_id)

    storeintowishlist = Wishlist(userid=user, productid = Product)
    storeintowishlist.save()
    messages.success(request,"Product added to wishlist")
    return redirect('/')

def displaywishlist(request):
    product = Wishlist.objects.all()
    context = {
        "product":product
    }
    return render(request,"wishlist.html",context)

def removewishlist(request, id):
    login_id = request.session.get("log_id")

    Wishlist.objects.filter(userid_id=login_id, productid_id=id).delete()

    messages.success(request, "Item removed from wishlist")
    return redirect(displaywishlist)


def forgotpasswordpage(request):
    return render(request,"forgotpass.html")

def forgotpassword(request):
   if request.method == 'POST':
       username = request.POST.get('email')
       try:
           user = RegisterModel.objects.get(email=username)
       except RegisterModel.DoesNotExist:
           user = None


       if user is not None:
           import random


           letters = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
           numbers = list('0123456789')
           symbols = list('!#$%&()*+')


           password_list = []


           for _ in range(6):
               password_list.append(random.choice(letters))


           for _ in range(1):
               password_list.append(random.choice(symbols))


           for _ in range(3):
               password_list.append(random.choice(numbers))


           random.shuffle(password_list)


           password = "".join(password_list)


           msg = "hello here it is your new password " + password


           from django.core.mail import send_mail


           send_mail(
               'Your New Password',
               msg,
               'parthinfolabz19@gmail.com',
               [username],
               fail_silently=False,
           )


           user = RegisterModel.objects.get(email=username)
           user.password = password
           user.save(update_fields=['password'])


           messages.info(request, 'Mail is sent')
           return redirect(login)
       else:
           messages.info(request, 'This account does not exist')
           return redirect(login)




   return render(request, "login.html")



def vieworder(request, id):
   user_id = request.session['log_id']

   # order = Order.objects.get(id=id, userid_id=user_id)
   order = Order.objects.filter(id=id, userid=RegisterModel(id=user_id))

   products = Cart.objects.filter(
       userid_id=user_id,
       orderid=id,
       orderstatus=0
   )


   context = {
       'order': order,
       'order_details': products
   }


   return render(request, 'vieworders.html', context)




