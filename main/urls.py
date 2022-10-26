"""LeeBeauty URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),

    path("provinces/", views.provinces, name="provinces"),
    path("districts/", views.districts, name="districts"),
    path("communes/", views.communes, name="communes"),

    path("account", views.account, name="account"),
    path("sign-in/", views.signin, name="signin"),
    path("sign-up/", views.signup, name="signup"),
    path("sign-out/", views.signout, name="signout"),

    path("sync-cart/", views.sync_cart, name="sync_cart"),

    path("<str:category_id>/", views.category, name="category"),
    path("product/<str:product_id>/", views.product, name="product"),
    
    path("more_products/<str:category_id>/<int:page>/", views.more_products, name="more_products"),


]
