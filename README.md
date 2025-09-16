# Transfer Market

Tautan pws: https://walyulahdi-maulana-transfermarket.pbp.cs.ui.ac.id/

## Tugas 2

### Step-by-step Implementasi Checklist (Tugas 2)

1. Saya membuat proyek Django baru dengan menjalankan command

   ```bash
   django-admin startproject transfer_market
   ```

2. Membuat aplikasi main dengan command

   ```bash
   python manage.py startapp main
   ```

   kemudian menambahkan `'main'` ke dalam `INSTALLED_APP` pada `settings.py`.

3. Melakukan routing main dengan menambahkan

   ```python
   path('', include('main.urls'))
   ```

   pada `transfer_market/urls.py`.

4. Membuat model Product pada `main/models.py`

   ```python
   class Product(models.Model):
       name = models.CharField()
       price = models.IntegerField()
       description = models.TextField()
       thumbnail = models.URLField()
       category = models.CharField()
       is_featured = models.BooleanField()
       rating = models.FloatField()
   ```

5. Membuat fungsi pada `main/views.py`
   ```python
   def show_main(request):
       context = {
           'name' : 'Walyul\'ahdi Maulana Ramadhan',
           'npm' : '2406426012',
           'class' : 'PBP - F'
       }
       return render(request, "main.html", context)
   ```
6. Melakukan routing juga pada `main/urls.py`, dengan menambahkan
   ```python
   urlpatterns = [
       path('', show_main, name='show_main'),
   ]
   ```

### Bagan

![Bagan](assets/readme/bagan.png)

### Peran settings.py dalam proyek Django

Mengatur konfigurasi proyek, seperti:

- INSTALLED_APP  
  Daftar aplikasi yang digunakan
- DATABASES  
  Koneksi ke database
- TEMPLATES  
  Konfigurasi template
- ALLOWED_HOSTS  
  Daftar host yang mempunyai akses

### Cara kerja migrasi database di Django

1. Saat menambah dan mengubah model menjalankan command

   ```bash
   python manage.py makemigrations
   ```

   File migrasi dibuat berdasarkan perubahan pada `models.py`.

2. Saat ingin menerapkan perubahan ke database menjalancan command

   ```bash
   python manage.py migrate
   ```

   Django mengeksekusi migrasi yang belum diterapkan di database.

3. Django menyimpan track migrasi yang sudah diterapkan di tabel `django_migrations`.

### Mengapa framework Django dijadikan permulaan pembelajaran pengembangan perangkat lunak?

Django dijadikan permulaan pembelajaran karena menyediakan fitur bawaan yang lengkap seperti ORM, autentikasi, dan admin panel tanpa membangun semua dari nol. Pola MVT pada Django juga cukup memudahkan dalam memahami konsep pengembangan perangkat lunak secara terstruktur. Selain itu, kami sudah familiar dengan bahasa pemrograman python sejak semester pertama.

### Feedback Tutorial 1

Menurut saya semua penjelasan step-by-step pada tutorial sudah jelas, sehingga saya dapat mengikuti dengan baik.

## Tugas 3

### Mengapa kita memerlukan data delivery dalam pengimplementasian sebuah platform?

Data delivery diperlukan untuk memastikan data dapat ditransfer dengan aman dari server ke klien. Data delivery memungkinkan pertukaran informasi dalam format seperti XML dan JSON, serta memungkikan untuk melayani banyak klien secara bersamaan.

### JSON vs XML

JSON umumnya lebih disukai karena formatnya yang lebih ringkas, mudah dibaca, dan lebih cepat di-parse dibanding XML. Selain itu JSON juga didukung secara native di JavaScript yang merupakan bahasa utama pengembangan web.

### Fungsi dari method `is_valid()` pada form Django dan mengapa dibutuhkan?

Method `is_valid()` berfungsi untuk memvalidasi data input pengguna sesuai aturan yang ditentukan dalam form dan model dan Memastikan bahwa semua field yang wajib diisi sudah terisi. Method ini dibutuhkan untuk memastikan data yang akan disimpan ke database bersih dan aman sesuai aturan.

### Peran `csrf_token` pada form di Django, Apa yang terjadi jika tidak ada? dan Bagaimana hal tersebut dapat dimanfaatkan oleh penyerang?

`csrf_token` berperan untuk melindungi website dari serangan CSRF Cross-Site Request Forgery. Tanpa `csrf_token`, penyerang dapat membuat web palsu yang mengirimkan request ke web kita tanpa sepengetahuan user. 

### Step-by-step Implementasi Checklist (Tugas 3)

1. Menambahkan 4 fungsi baru pada `views.py`

   ```python
   def show_xml(request):
      product_list = Product.objects.all()
      xml_data = serializers.serialize("xml", product_list)
      return HttpResponse(xml_data, content_type="application/xml")

   def show_json(request):
      product_list = Product.objects.all()
      json_data = serializers.serialize("json", product_list)
      return HttpResponse(json_data, content_type="application/json")

   def show_xml_by_id(request, product_id):
      try:
         product_item = Product.objects.filter(pk=product_id)
         xml_data = serializers.serialize("xml", product_item)
         return HttpResponse(xml_data, content_type="application/xml")
      except Product.DoesNotExist:
         return HttpResponse(status=404)

   def show_json_by_id(request, product_id):
      try:
         product_item = Product.objects.get(pk=product_id)
         json_data = serializers.serialize("json", [product_item])
         return HttpResponse(json_data, content_type="application/json")
      except Product.DoesNotExist:
         return HttpResponse(status=404)
   ```

2. Membuat routing URL untuk 4 fungsi tersebut pada `main/urls.py`

   ```python
      path('xml/', show_xml, name='show_xml'),
      path('json/', show_json, name='show_json'),
      path('xml/<str:product_id>/', show_xml_by_id, name='show_xml_by_id'),
      path('json/<str:product_id>/', show_json_by_id, name='show_json_by_id'),
   ```

3. Menambahkan field baru pada model `Product` di `main/models.py`

   ```python
      id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
   ```

4. Membuat halaman baru `create_product.html` dan `product_detail.html` pada direktori`main/templates`

5. Membuat fungsi `create_product` dan `show_product` pada `views.py`

   ```python
   def create_product(request):
      form = ProductForm(request.POST or None)

      if form.is_valid() and request.method == "POST":
         form.save()
         return redirect("main:show_main")

      context = {'form': form}
      return render(request, "create_product.html", context)


   def show_product(request, id):
      product = get_object_or_404(Product, pk=id)

      context = {'product': product}

      return render(request, "product_detail.html", context)
    ```

6. Membuat routing URL untuk 4 fungsi tersebut pada `main/urls.py`

   ```python
      path('create-product/', create_product, name='create_product'),
      path('product/<str:id>/', show_product, name='show_product'),
   ```

### Feedback Tutorial 2

Tutorial 2 sudah cukup jelas dan membantu memahami konsep Form dan Data Delivery pada Django. Tetapi saya belum terlalu memahami terkait csrf.

### Mengakses Keempat URL di poin 2 (Postman)

1. XML
   ![XML](assets/readme/postman_xml.png)

2. JSON
   ![JSON](assets/readme/postman_json.png)

3. XML By ID
   ![XML By Id](assets/readme/postman_xml_by_id.png)

4. JSON
   ![JSON By Id](assets/readme/postman_json_by_id.png)
