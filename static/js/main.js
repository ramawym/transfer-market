$(document).ready(function () {
  let currentFilter = "all";

  // --- FUNGSI UTILITAS ---
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  const csrftoken = getCookie("csrftoken");

  // Fungsi showToast tidak perlu diubah
  function showToast(message, type = "success") { /* ... (kode toast Anda) ... */ }

  // --- PENGELOLAAN PRODUK ---
  function fetchProducts() {
    $("#product-container").html(`<div class="col-span-full text-center p-8"><p class="text-gray-500">Loading products... ⏳</p></div>`);
    $.ajax({
      url: `/get-product/?filter=${currentFilter}`,
      type: "GET",
      success: function (data) {
        const products = JSON.parse(data);
        $("#product-container").empty();
        if (products.length === 0) {
          $("#product-container").html(`<div class="col-span-full bg-white rounded-lg border border-gray-200 p-12 text-center"><p class="text-gray-500 mb-6">No products found. Add a new one!</p></div>`);
          return;
        }
        products.forEach(function (product) {
          const card = `
            <div class="bg-white rounded-lg border border-gray-200 overflow-hidden shadow-sm hover:shadow-lg transition-shadow duration-300">
                <img src="${product.fields.thumbnail || "https://placehold.co/600x400"}" alt="${product.fields.name}" class="w-full h-48 object-cover">
                <div class="p-4">
                    <h3 class="text-lg font-semibold text-gray-800 mb-2">${product.fields.name}</h3>
                    <p class="text-gray-600 text-sm mb-4 truncate">${product.fields.description}</p>
                    <div class="flex items-center justify-between">
                        <span class="text-xl font-bold text-blue-600">$${product.fields.price}</span>
                        <div class="flex gap-2">
                             <button class="edit-btn text-yellow-500 hover:text-yellow-700" data-id="${product.pk}">Edit</button>
                             <button class="delete-btn text-red-500 hover:text-red-700" data-id="${product.pk}">Delete</button>
                        </div>
                    </div>
                </div>
            </div>`;
          $("#product-container").append(card);
        });
      },
      error: function () {
        $("#product-container").html(`<div class="col-span-full text-center p-8"><p class="text-red-500">Error loading products. Please try again. 🚨</p></div>`);
      },
    });
  }

  // --- EVENT LISTENERS ---

  // Tombol di Navbar dan di Halaman Utama untuk Buka Modal Create
  // Menggunakan class selector agar bisa mentarget banyak tombol
  $(document).on("click", ".create-product-trigger", function () {
    $("#create-product-modal").removeClass("hidden");
  });

  // Tombol Close di semua modal
  $(document).on("click", ".close-modal", function () {
    $(this).closest(".modal").addClass("hidden");
  });

  // Submit Form Create Product
  $("#create-product-form").submit(function (e) {
    e.preventDefault();
    $.ajax({
      type: "POST",
      url: "/create-product-ajax/",
      data: $(this).serialize(),
      beforeSend: (xhr) => xhr.setRequestHeader("X-CSRFToken", csrftoken),
      success: function (response) {
        $("#create-product-modal").addClass("hidden");
        $("#create-product-form")[0].reset();
        showToast(response.message, "success");
        fetchProducts();
      },
      error: () => showToast("An error occurred. Please check your input.", "error"),
    });
  });

  // Refresh, Filter, dan Fetch Awal
  $("#refresh-products").click(fetchProducts);
  $("#filter-tabs").on("click", ".filter-btn", function () {
    currentFilter = $(this).data("filter");
    $(".filter-btn").removeClass("border-blue-600 text-blue-600").addClass("border-transparent text-gray-500");
    $(this).addClass("border-blue-600 text-blue-600").removeClass("border-transparent text-gray-500");
    fetchProducts();
  });
  fetchProducts();

  // BARU: Logout via AJAX
  $(document).on('click', '.logout-btn', function(e) {
    e.preventDefault();
    $.ajax({
        type: "POST",
        url: "/logout-ajax/",
        beforeSend: (xhr) => xhr.setRequestHeader("X-CSRFToken", csrftoken),
        success: function (response) {
            showToast(response.message, 'success');
            setTimeout(() => {
                window.location.href = '/login/';
            }, 1500);
        },
        error: () => showToast('Logout failed. Please try again.', 'error'),
    });
  });

  // BARU: Fungsionalitas Delete Product
  // 1. Saat tombol delete di kartu produk diklik
  $('#product-container').on('click', '.delete-btn', function() {
    const productId = $(this).data('id');
    // Simpan ID produk di tombol konfirmasi modal untuk digunakan nanti
    $('#confirm-delete-btn').data('productId', productId);
    // Tampilkan modal konfirmasi
    $('#delete-confirm-modal').removeClass('hidden');
  });

  // 2. Saat tombol konfirmasi delete di dalam modal diklik
  $('#confirm-delete-btn').on('click', function() {
    const productId = $(this).data('productId');
    $.ajax({
        type: "POST",
        url: `/delete-product-ajax/${productId}/`,
        beforeSend: (xhr) => xhr.setRequestHeader("X-CSRFToken", csrftoken),
        success: function(response) {
            $('#delete-confirm-modal').addClass('hidden');
            showToast(response.message, 'success');
            fetchProducts(); // Muat ulang daftar produk
        },
        error: function() {
            $('#delete-confirm-modal').addClass('hidden');
            showToast('Failed to delete product.', 'error');
        }
    });
  });
});