from django.urls import path
from main.views import (
    show_main_html, 
    show_main, 
    create_product, 
    show_product,
    show_products_xml,
    show_products_json, 
    show_product_xml_by_id,
    show_product_json_by_id,
    register, 
    login_user, 
    logout_user, 
    edit_product, 
    delete_product,
    add_product_entry_ajax, 
    proxy_image, 
    create_product_flutter
)


app_name = "main"

urlpatterns = [
    path("", show_main_html, name="show_main"),
    # Product CRUD paths
    path("create-product/", create_product, name="create_product"),
    path("product/<uuid:id>/", show_product, name="show_product"),
    path('product/<uuid:id>/edit', edit_product, name='edit_product'), 
    path('product/<uuid:id>/delete', delete_product, name='delete_product'), 
    path("get-product/", show_main, name="get_product_list"),

    # API paths
    path('xml/', show_products_xml, name='show_products_xml'), 
    path('json/', show_products_json, name='show_products_json'), 
    path('xml/<uuid:product_id>/', show_product_xml_by_id, name='show_product_xml_by_id'), 
    path('json/<uuid:product_id>/', show_product_json_by_id, name='show_product_json_by_id'), 
    
    # User auth paths
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    
    # AJAX and Flutter paths
    path('create-product-ajax', add_product_entry_ajax, name='add_product_entry_ajax'), 
    path('proxy-image/', proxy_image, name='proxy_image'),
    path('create-flutter/', create_product_flutter, name='create_product_flutter'), 
]