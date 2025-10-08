# main/urls.py

from django.urls import path
from main.views import (
    # Views untuk Halaman (HTML)
    show_main,
    register,
    login_user,

    # Endpoints untuk AJAX (JSON)
    get_product_json,
    create_product_ajax,
    edit_product_ajax,
    delete_product_ajax,
    register_ajax,
    login_ajax,
    logout_ajax,
)

app_name = "main"

urlpatterns = [
    # === Rute untuk Halaman ===
    path("", show_main, name="show_main"),
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),

    # === Endpoints untuk Fungsionalitas AJAX ===
    # Otentikasi
    path("register-ajax/", register_ajax, name="register_ajax"),
    path("login-ajax/", login_ajax, name="login_ajax"),
    path("logout-ajax/", logout_ajax, name="logout_ajax"),

    # CRUD Produk
    path("get-product/", get_product_json, name="get_product_json"),
    path("create-product-ajax/", create_product_ajax, name="create_product_ajax"),
    path("edit-product-ajax/<uuid:id>/", edit_product_ajax, name="edit_product_ajax"),
    path("delete-product-ajax/<uuid:id>/", delete_product_ajax, name="delete_product_ajax"),
]