"""
URL configuration for p1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from app1 import views

urlpatterns = [
   path('admin/', admin.site.urls),
   path('register',views.register),
   path('registerdata',views.registerdata),
   path('login',views.login),
   path('logindata',views.logindata),
   path('logout/', views.logout),
   path('', views.show),
   path('addpro',views.addpro),
   path('insertpro',views.insertpro),
   path('singleproduct/<int:id>',views.singleproduct),
   path('catvisepro/<int:id>',views.catvisepro),
   path('exclude',views.exclude),
   path('sort',views.sort),
   path('showcount',views.showcount),
   path('showvalues',views.showvalues),
   path('aggregation',views.aggregation),
   path('selectrelated',views.showselectrelated),
   path('showcolor',views.showcolor),
   path('singleproductnew/<int:id>',views.singleproductnew),
   path('insertcart',views.insertcart),
   path('cart',views.cart),
   path('deletecart/<int:id>',views.deletecart),
   path('increase/<int:id>',views.increase),
   path('decrease/<int:id>',views.decrease),
   path('manageproduct',views.manageproduct),
   path('deleteproduct/<int:id>',views.deleteproduct),
   path('editproduct/<int:id>',views.editproduct),
   path('updatedata',views.updatedata),
   path('placeorder',views.placeorder),
   path('payment_success',views.payment_success),
   path('myorder',views.myorder),

    path('sellerorders',views.sellerorders),
    path('addwishlist/<int:id>',views.addwishlist),
    path('displaywishlist',views.displaywishlist),
    path('removewishlist/<int:id>',views.removewishlist),
    path('forgotpasswordpage/',views.forgotpasswordpage),
    path('forgotpassword/',views.forgotpassword),
    path('vieworders/<int:id>',views.vieworder),

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

