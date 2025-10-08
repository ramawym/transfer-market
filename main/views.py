# main/views.py

import datetime
import json
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from main.forms import ProductForm
from main.models import Product

# =====================================================================
# VIEWS UNTUK MENAMPILKAN HALAMAN (MERENDER HTML)
# =====================================================================

def register(request):
    """Menampilkan halaman registrasi."""
    form = UserCreationForm()
    return render(request, "register.html", {"form": form})

def login_user(request):
    """Menampilkan halaman login."""
    form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

@login_required(login_url="/login/")
def show_main(request):
    """Menampilkan halaman utama setelah login."""
    context = {
        "last_login": request.COOKIES.get("last_login", "Never"),
    }
    return render(request, "main.html", context)

# =====================================================================
# ENDPOINTS UNTUK AJAX (MENGEMBALIKAN JSON)
# =====================================================================

@csrf_exempt
def register_ajax(request):
    """Memproses data registrasi dari permintaan AJAX."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success', 'message': 'Registration successful! Please login.'}, status=201)
        else:
            errors = {field: error[0] for field, error in form.errors.items()}
            return JsonResponse({'status': 'error', 'errors': errors}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

@csrf_exempt
def login_ajax(request):
    """Memproses data login dari permintaan AJAX."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = JsonResponse({"status": "success", "message": "Login successful!"})
            response.set_cookie("last_login", str(datetime.datetime.now()))
            return response
        else:
            return JsonResponse({"status": "error", "message": "Invalid username or password"}, status=401)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

@csrf_exempt
def logout_ajax(request):
    """Memproses logout dari permintaan AJAX."""
    if request.method == "POST":
        logout(request)
        response = JsonResponse({"status": "success", "message": "You have been logged out."})
        response.delete_cookie("last_login")
        return response
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

@login_required
def get_product_json(request):
    """Mengambil data produk dalam format JSON."""
    filter_type = request.GET.get("filter", "all")
    if filter_type == "my":
        products = Product.objects.filter(user=request.user)
    else:
        products = Product.objects.all()
    return HttpResponse(serializers.serialize('json', products))

@login_required
@csrf_exempt
def create_product_ajax(request):
    """Memproses pembuatan produk baru via AJAX."""
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return JsonResponse({"status": "success", "message": "Product added successfully!"}, status=201)
        else:
            return JsonResponse({"status": "error", "errors": form.errors}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

@login_required
@csrf_exempt
def edit_product_ajax(request, id):
    """Memproses pembaruan produk via AJAX."""
    if request.method == "POST":
        product = get_object_or_404(Product, pk=id, user=request.user)
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return JsonResponse({"status": "success", "message": "Product updated successfully!"})
        else:
            return JsonResponse({"status": "error", "errors": form.errors}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

@login_required
@csrf_exempt
def delete_product_ajax(request, id):
    """Memproses penghapusan produk via AJAX."""
    if request.method == "POST":
        try:
            product = get_object_or_404(Product, pk=id, user=request.user)
            product.delete()
            return JsonResponse({"status": "success", "message": "Product deleted successfully!"})
        except Product.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Product not found or you don't have permission."}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)
