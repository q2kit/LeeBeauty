from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.db.models import Q

from .models import *
from .validate import *

import hashlib
import json

# Create your views here.


def provinces(request):
    provinces = Province.objects.all()
    return JsonResponse(
        {"success": True, "provinces": [province.to_json() for province in provinces]},
        status=200,
    )


def districts(request):
    try:
        province_id = request.GET.get("province_id")
        province = Province.objects.get(id=province_id)
        districts = District.objects.filter(province=province)
        return JsonResponse(
            {
                "success": True,
                "districts": [district.to_json() for district in districts],
            },
            status=200,
        )
    except:
        return JsonResponse(
            {"success": False, "message": "Invalid province_id"},
            status=400,
        )


def communes(request):
    try:
        district_id = request.GET.get("district_id")
        district = District.objects.get(id=district_id)
        communes = Commune.objects.filter(district=district)
        return JsonResponse(
            {
                "success": True,
                "communes": [commune.to_json() for commune in communes],
            },
            status=200,
        )
    except:
        return JsonResponse(
            {"success": False, "message": "Invalid district_id"},
            status=400,
        )


def num_in_cart(request):
    try:
        uid = request.session["uid"]
        user = User.objects.get(id=uid)
        return len(CartProduct.objects.filter(user=user))
    except:
        return 0


def index(request):
    data = {
        "categories": categories(),
        "products": get_products(numperpage=30),
        "num_in_cart": num_in_cart(request),
    }

    return render(request, "index.html", data)


def account(request):
    if request.method == "GET":
        try:
            uid = request.session["uid"]
            user = User.objects.get(id=uid)
            return render(request, "account.html", {"user": user})
        except:
            return redirect("/sign-in?next=/account")

    else:
        return JsonResponse(
            {"status": "error", "message": "Method not allowed"}, status=405
        )


def signin(request):
    if request.method == "GET":
        uid = request.session.get("uid")
        if uid:
            return redirect("/")
        return render(request, "signin.html")
    elif request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(Q(email=email) | Q(phone=email))
            if user.password == hashlib.sha256(password.encode()).hexdigest():
                request.session["uid"] = user.id
                return JsonResponse(
                    {"success": True, "message": "Đăng nhập thành công"}, status=200
                )
            else:
                return JsonResponse(
                    {"success": False, "message": "Mật khẩu không chính xác"},
                    status=400,
                )
        except:
            return JsonResponse(
                {"success": False, "message": "Tài khoản không tồn tại"}, status=400
            )
    else:
        return JsonResponse(
            {"status": "error", "message": "Method not allowed"}, status=405
        )


def signup(request):
    if request.method == "GET":
        return render(request, "signup.html")
    elif request.method == "POST":
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        if not validate_email(email):
            return JsonResponse(
                {"success": False, "message": "Email không hợp lệ"}, status=400
            )
        if not validate_phone(phone):
            return JsonResponse(
                {"success": False, "message": "Số điện thoại không hợp lệ"},
                status=400,
            )
        if not validate_password(password):
            return JsonResponse(
                {"success": False, "message": "Mật khẩu không hợp lệ"}, status=400
            )

        try:
            user = User.objects.get(Q(email=email) | Q(phone=phone))
            return JsonResponse(
                {
                    "success": False,
                    "message": "Email hoặc số điện thoại đã được sử dụng",
                },
                status=400,
            )
        except:
            user = User.objects.create(
                email=email,
                phone=phone,
                password=hashlib.sha256(password.encode()).hexdigest(),
            )
            request.session["uid"] = user.id
            return JsonResponse(
                {"success": True, "message": "Đăng ký thành công"}, status=200
            )
    else:
        return JsonResponse(
            {"success": "False", "message": "Method not allowed"}, status=405
        )


def signout(request):
    if request.method == "GET":
        try:
            del request.session["uid"]
            return redirect("/sign-in")
        except:
            return redirect("/sign-in")
    else:
        return JsonResponse(
            {"status": "error", "message": "Method not allowed"}, status=405
        )


def product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        return render(request, "product.html", {"product": product})
    except:
        return redirect("/")


def category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)

        data = {
            "categories": categories(),
            "products": get_products(category=category),
            "num_in_cart": num_in_cart(request),
        }

        return render(request, "index.html", data)
    except Exception as e:
        print(e)
        return redirect("/")


def get_products(category=None, page=0, numperpage=20):
    if category:
        products = Product.objects.filter(category=category)
        for sub_categorie in category.sub_categories:
            products = products | Product.objects.filter(category=sub_categorie)
        return products[page * numperpage : (page + 1) * numperpage]
    else:
        products = Product.objects.all()
        return products[page * numperpage : (page + 1) * numperpage]


def categories():
    return [category for category in Category.objects.all() if category.parent is None]


def more_products(request, category_id, page):
    try:
        category = Category.objects.get(id=category_id)
    except:
        category = None

    products = get_products(category, page)
    if not products:
        return JsonResponse({"success": False, "message": "Không còn sản phẩm"})
    return JsonResponse(
        {
            "success": True,
            "products": products,
        },
        status=200,
    )


def sync_cart(request):
    if request.method == "POST":
        try:
            uid = request.session["uid"]
            user = User.objects.get(id=uid)

            cart = request.POST.get("cart")
            cart = json.loads(cart)
            print(cart)


            for item in cart:
                product_id = item["product_id"]
                quantity = item["quantity"]
                size = item["size"]
                color = item["color"]

                product = Product.objects.get(id=product_id)
                product_detail = ProductDetail.objects.get(
                    product=product, size=size, color=color
                )

                CartProduct.objects.create(
                    user=user,
                    product_detail=product_detail,
                    quantity=quantity,
                )

            return JsonResponse(
                {"success": True, "message": "Đồng bộ thành công"}, status=200
            )
        except Exception as e:
            return JsonResponse(
                {"success": False, "message": "Đồng bộ thất bại"}, status=400
            )

    else:
        return JsonResponse(
            {"success": False, "message": "Method not allowed"}, status=405
        )
