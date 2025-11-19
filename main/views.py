from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404
# from main.forms import NewsForm # Assuming you will create a ProductForm
from main.models import Product # Changed from News to Product
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import datetime
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
import requests
import json
from django import forms

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "description", "thumbnail", "category", "is_featured"]



# Create your views here.
@login_required(login_url="/login")
def show_main_html(request):
    filter_type = request.GET.get("filter", "all")

    if filter_type == "all":
        product_list = Product.objects.all()
    else:
        product_list = Product.objects.filter(user=request.user)

    context = {
        "npm": "2406426012",
        "name": "Walyulahdi Maulana Ramadhan",
        "class": "PBP F",
        "product_list": product_list,
        "last_login": request.COOKIES.get("last_login", "Never"),
    }

    return render(request, "main.html", context)

@login_required(login_url="/login")
def show_main(request): # Re-use the name for the client's URL
    filter_type = request.GET.get("filter", "all")
    if filter_type == "all":
        product_list = Product.objects.all()
    else:
        product_list = Product.objects.filter(user=request.user)

    # Return JSON data instead of rendering HTML
    data = [
        {
            "id": str(p.id),
            "name": p.name,
            "price": p.price,
            "category": p.category,
            "is_featured": p.is_featured,
            # Add other necessary fields
        }
        for p in product_list
    ]
    return JsonResponse({"products": data}, safe=False)


@login_required(login_url="/login")
def create_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        product_entry = form.save(commit=False)
        product_entry.user = request.user
        product_entry.save()
        return redirect("main:show_main")

    context = {"form": form}
    return render(request, "create_product.html", context)


@login_required(login_url="/login")
def edit_product(request, id):
    product = get_object_or_404(Product, pk=id)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid() and request.method == "POST":
        form.save()
        # Changed redirection name
        return redirect("main:show_main")

    context = {"form": form}

    # Assuming edit_product.html template exists or can be created
    return render(request, "edit_product.html", context)


# Changed function name from delete_news to delete_product
@login_required(login_url="/login")
def delete_product(request, id):
    # Changed News to Product
    product = get_object_or_404(Product, pk=id)
    product.delete()
    # Changed redirection name
    return HttpResponseRedirect(reverse("main:show_main"))


# Changed function name from show_news to show_product
@login_required(login_url="/login")
def show_product(request, id):
    # Changed News to Product
    product = get_object_or_404(Product, pk=id)
    # Removed increment_views() since Product model does not have news_views field
    
    context = {"product": product}

    # Assuming product_detail.html template exists or can be created
    return render(request, "product_detail.html", context)


# Changed function name from show_xml to show_products_xml
def show_products_xml(request):
    # Changed News.objects.all() to Product.objects.all()
    product_list = Product.objects.all()
    xml_data = serializers.serialize("xml", product_list)
    return HttpResponse(xml_data, content_type="application/xml")


# Changed function name from show_json to show_products_json
def show_products_json(request):
    # Changed News.objects.all() to Product.objects.all()
    product_list = Product.objects.all()
    data = [
        {
            "id": str(product.id),
            "name": product.name, # Changed from title
            "price": product.price, # New field
            "description": product.description, # Changed from content
            "category": product.category,
            "thumbnail": product.thumbnail,
            "is_featured": product.is_featured,
            "rating": product.rating, # New field
            "user_id": product.user_id,
        }
        for product in product_list
    ]

    return JsonResponse(data, safe=False)


def show_product_xml_by_id(request, product_id):
    try:
        product_item = Product.objects.filter(pk=product_id)
        xml_data = serializers.serialize("xml", product_item)
        return HttpResponse(xml_data, content_type="application/xml")
    except Product.DoesNotExist: 
        return HttpResponse(status=404)


def show_product_json_by_id(request, product_id):
    try:
        product = Product.objects.select_related("user").get(pk=product_id)
        data = {
            "id": str(product.id),
            "name": product.name, 
            "price": product.price,
            "description": product.description, 
            "category": product.category,
            "thumbnail": product.thumbnail,
            "is_featured": product.is_featured,
            "rating": product.rating,
            "user_id": product.user_id,
            "user_username": product.user.username if product.user_id else None,
        }
        return JsonResponse(data)
    except Product.DoesNotExist:
        return JsonResponse({"detail": "Not found"}, status=404)


def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been successfully created!")
            return redirect("main:login")
    context = {"form": form}
    return render(request, "register.html", context)


def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie("last_login", str(datetime.datetime.now()))
            return response

    else:
        form = AuthenticationForm(request)
    context = {"form": form}
    return render(request, "login.html", context)


def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse("main:login"))
    response.delete_cookie("last_login")
    return response


@csrf_exempt
@require_POST
@login_required(login_url="/login") 
def add_product_entry_ajax(request):
    name = strip_tags(request.POST.get("name"))
    description = strip_tags(request.POST.get("description"))
    price_str = request.POST.get("price")
    category = request.POST.get("category")
    thumbnail = request.POST.get("thumbnail")
    is_featured = request.POST.get("is_featured") == "on"  # checkbox handling
    # Rating field is not included in the AJAX for simplicity, assuming default 0
    user = request.user

    try:
        price = int(price_str)
    except (TypeError, ValueError):
        price = 0 # Default price if conversion fails

    new_product = Product(
        name=name,
        price=price,
        description=description,
        category=category,
        thumbnail=thumbnail,
        is_featured=is_featured,
        user=user,
    )
    new_product.save()

    return HttpResponse(b"CREATED", status=201)


def proxy_image(request):
    image_url = request.GET.get("url")
    if not image_url:
        return HttpResponse("No URL provided", status=400)

    try:
        # Fetch image from external source
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()

        # Return the image with proper content type
        return HttpResponse(
            response.content,
            content_type=response.headers.get("Content-Type", "image/jpeg"),
        )
    except requests.RequestException as e:
        return HttpResponse(f"Error fetching image: {str(e)}", status=500)


@csrf_exempt
@login_required(login_url="/login") 
def create_product_flutter(request):
    if request.method == "POST":
        data = json.loads(request.body)
        name = strip_tags(data.get("name", ""))
        description = strip_tags(data.get("description", "")) 
        price = data.get("price", 0)
        category = data.get("category", "")
        thumbnail = data.get("thumbnail", "")
        is_featured = data.get("is_featured", False)
        # Rating field is not included for simplicity
        user = request.user

        new_product = Product(
            name=name,
            price=price,
            description=description,
            category=category,
            thumbnail=thumbnail,
            is_featured=is_featured,
            user=user,
        )
        new_product.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405) 