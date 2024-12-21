from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json

from .models import Category, Product, UnitType

# TODO: product detail page
# TODO: add pagination, filtering, ordering to product list page
# TODO: 

@login_required
def category(request):
    category_list = Category.objects.all()
    context = {
        "page_title": "Category List",
        "category": category_list,
    }
    return render(request, "pos/category.html", context)


@login_required
def manage_category(request):
    category = {}
    if request.method == "GET":
        data = request.GET
        id = ""
        if "id" in data:
            id = data["id"]
        if id.isnumeric() and int(id) > 0:
            category = Category.objects.filter(id=id).first()

    context = {"category": category}
    return render(request, "pos/manage_category.html", context)


@login_required
def save_category(request):
    data = request.POST
    resp = {"status": "failed"}
    try:
        if (data["id"]).isnumeric() and int(data["id"]) > 0:
            save_category = Category.objects.filter(id=data["id"]).update(
                name=data["name"],
                description=data["description"],
                status=data["status"],
            )
        else:
            save_category = Category(
                name=data["name"],
                description=data["description"],
                status=data["status"],
            )
            save_category.save()
        resp["status"] = "success"
        messages.success(request, "Category Successfully saved.")
    except:
        resp["status"] = "failed"
    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def delete_category(request):
    data = request.POST
    resp = {"status": ""}
    try:
        Category.objects.filter(id=data["id"]).delete()
        resp["status"] = "success"
        messages.success(request, "Category Successfully deleted.")
    except:
        resp["status"] = "failed"
    return HttpResponse(json.dumps(resp), content_type="application/json")


# Products
@login_required
def products(request):
    product_list = Product.objects.filter(category__status = True)
    context = {
        "page_title": "Product List",
        "products": product_list,
    }
    return render(request, "pos/products.html", context)


@login_required
def manage_products(request):
    """
    This endpoint is used as modal.
    """
    product = {}
    categories = Category.active.all()
    unit_types = UnitType.objects.all()
    if request.method == "GET":
        data = request.GET
        id = ""
        if "id" in data:
            id = data["id"]
        if id.isnumeric() and int(id) > 0:
            product = Product.objects.filter(id=id).first()

    context = {"product": product, "categories": categories, "unit_types": unit_types}
    return render(request, "pos/manage_product.html", context)


@login_required
def save_product(request):
    """
    This endpoind is used for both creating new product or updating existing one.
    If id exists in POST data then it is UPDATE, otherwise it is INSERT.
    """
    data = request.POST
    resp = {"status": "failed"}
    id = ""
    if "id" in data:
        id = data["id"]
    if id.isnumeric() and int(id) > 0:
        check = Product.objects.exclude(id=id).filter(code=data["code"]).all()
    else:
        check = Product.objects.filter(code=data["code"]).all()

    if len(check) > 0:
        resp["msg"] = "Product Code Already Exists in the database"
    else:
        category = Category.objects.get(id=data["category_id"])
        unit_type = UnitType.objects.get(id=data["unit_type"])
        try:
            if id.isnumeric() and int(id) > 0:
                save_product = Product.objects.filter(id=int(id)).update(
                    code=data["code"],
                    category=category,
                    name=data["name"],
                    description=data["description"],
                    price=int(data["price"]),
                    status=data["status"],
                    quantity=data["quantity"],
                    unit_type=unit_type,
                )
            else:
                save_product = Product(
                    code=data["code"],
                    category=category,
                    name=data["name"],
                    description=data["description"],
                    price=int(data["price"]),
                    status=data["status"],
                    quantity=data["quantity"],
                    unit_type=unit_type,
                )
                save_product.save()
                print("product saved")
            resp["status"] = "success"
            messages.success(request, "Product Successfully saved.")
        except Exception as e:
            resp["status"] = "failed"
    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def delete_product(request):
    data = request.POST
    resp = {"status": ""}
    try:
        Product.objects.filter(id=data["id"]).delete()
        resp["status"] = "success"
        messages.success(request, "Product Successfully deleted.")
    except:
        resp["status"] = "failed"
    return HttpResponse(json.dumps(resp), content_type="application/json")
