from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib import messages
import json, sys

from inventory.models import Category, Product
from .models import Order, OrderItem

# TODO: subtract selected quantity from available quantity
# TODO: enrich admin panel
# TODO: change checkout page
# TODO: change print cheque page
# TODO: show available quantity
# TODO: add links to home page's card icons
# TODO: create page to see/update transactions. If the quantity changes, it should reflect to available quantity. Make cheque also.

# BUG: order items table overflow issue

# def load(request):
#     import csv
#     from inventory.models import UnitType


#     with open(r'D:\Python\Projects\pos\shop\products.csv', 'rt', encoding='utf8') as file:
#         reader = csv.DictReader(file)
#         for row in reader:
#             try:
#                 category = Category.objects.get(id=int(row['category']))
#                 unit_type = UnitType.objects.get(id=int(row['unit_type']))
#                 product = Product(
#                     code=row['code'],
#                     category=category,
#                     name=row['name'],
#                     description=row['description'],
#                     price=int(row['price']),
#                     quantity=int(row['quantity']),
#                     unit_type=unit_type
#                 )
#                 product.save()
#             except Exception:
#                 pass
#     return HttpResponse('success')


def login_user(request):
    logout(request)
    resp = {"status": "failed", "msg": ""}
    username = ""
    password = ""
    if request.POST:
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                resp["status"] = "success"
            else:
                resp["msg"] = "Incorrect username or password"
        else:
            resp["msg"] = "Incorrect username or password"
    return HttpResponse(json.dumps(resp), content_type="application/json")


# Logout
def logoutuser(request):
    logout(request)
    return redirect("/")


# Create your views here.
@login_required
def home(request):
    now = datetime.now()
    current_year = now.strftime("%Y")
    current_month = now.strftime("%m")
    current_day = now.strftime("%d")
    categories = len(Category.active.all())
    products = len(Product.active.filter(quantity__gt=0))
    transaction = len(
        Order.objects.filter(
            date_created__year=current_year,
            date_created__month=current_month,
            date_created__day=current_day,
        )
    )
    today_sales = Order.objects.filter(
        date_created__year=current_year,
        date_created__month=current_month,
        date_created__day=current_day,
    ).all()
    total_sales = sum(today_sales.values_list("total", flat=True))
    context = {
        "page_title": "Home",
        "categories": categories,
        "products": products,
        "transaction": transaction,
        "total_sales": total_sales,
    }
    return render(request, "pos/home.html", context)


@login_required
def pos(request):
    products = Product.active.filter(category__status=True, quantity__gt = 0)
    product_json = []
    for product in products:
        product_json.append(
            {
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "quantity": product.quantity,
                "unit_type": product.unit_type.long_name,
            }
        )
    context = {
        "page_title": "Point of Sale",
        "products": products,
        "product_json": json.dumps(product_json),
    }
    # return HttpResponse('')
    return render(request, "pos/pos.html", context)


@login_required
def checkout_modal(request):
    grand_total = 0
    if "grand_total" in request.GET:
        grand_total = request.GET["grand_total"]
    context = {
        "grand_total": grand_total,
    }
    return render(request, "pos/checkout.html", context)


@login_required
def save_pos(request):
    resp = {"status": "failed", "msg": ""}
    data = request.POST

    try:
        order = Order(salesman=request.user, total=data["grand_total"])
        order.save()
        i = 0
        for prod in data.getlist("product_id[]"):
            product_id = prod
            product = Product.objects.get(id=product_id)
            qty = data.getlist("qty[]")[i]
            price_actual = data.getlist("price_actual[]")[i]
            price_sold = data.getlist("price_sold[]")[i]
            total = float(qty) * int(price_sold)
            print(
                {
                    "order_id": order.id,
                    "product_id": product.id,
                    "qty": qty,
                    "price": price_sold,
                    "total": total,
                }
            )
            OrderItem(
                order=order,
                product=product,
                price_actual=price_actual,
                price_sold=price_sold,
                quantity=qty,
                total=total,
            ).save()
            product.quantity -= float(qty)
            product.save()
            i += 1
        resp["status"] = "success"
        resp["order_id"] = order.id
        messages.success(request, "Sale Record has been saved.")
    except Exception as e:
        print(e)
        resp["msg"] = "An error occured"
        print("Unexpected error:", sys.exc_info()[0])
    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def salesList(request):
    sales = Order.objects.all()
    sale_data = []
    for sale in sales:
        data = {}
        for field in sale._meta.get_fields(include_parents=False):
            if field.related_model is None:
                data[field.name] = getattr(sale, field.name)
        data["items"] = OrderItem.objects.filter(sale_id=sale).all()
        data["item_count"] = len(data["items"])
        if "tax_amount" in data:
            data["tax_amount"] = format(float(data["tax_amount"]), ".2f")
        # print(data)
        sale_data.append(data)
    # print(sale_data)
    context = {
        "page_title": "Sales Transactions",
        "sale_data": sale_data,
    }
    # return HttpResponse('')
    return render(request, "pos/sales.html", context)


@login_required
def receipt(request):
    id = request.GET.get("id")
    order = Order.objects.get(id=id)
    transaction = {}
    for field in Order._meta.get_fields():
        if field.related_model is None:
            transaction[field.name] = getattr(order, field.name)

    item_list = order.order_items.all()
    context = {"transaction": transaction, "sales_items": item_list}

    return render(request, "pos/receipt.html", context)


@login_required
def delete_sale(request):
    resp = {"status": "failed", "msg": ""}
    id = request.POST.get("id")
    try:
        delete = Order.objects.filter(id=id).delete()
        resp["status"] = "success"
        messages.success(request, "Sale Record has been deleted.")
    except:
        resp["msg"] = "An error occured"
        print("Unexpected error:", sys.exc_info()[0])
    return HttpResponse(json.dumps(resp), content_type="application/json")
