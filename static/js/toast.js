function showToast(message, type = "success") {
  const toastContainer = document.getElementById("toast-container");
  if (!toastContainer) return;

  // Tentukan warna berdasarkan tipe
  const bgColor = type === "success" ? "bg-green-500" : "bg-red-500";

  // Buat elemen toast baru
  const toast = document.createElement("div");
  toast.className = `toast ${bgColor} text-white py-2 px-4 rounded-lg shadow-md mb-2 opacity-0 transform translate-x-10 transition-all duration-300`;
  toast.textContent = message;

  // Tambahkan ke container
  toastContainer.appendChild(toast);

  // Animasi masuk
  setTimeout(() => {
    toast.classList.remove("opacity-0", "translate-x-10");
  }, 10);

  // Animasi keluar setelah 3 detik
  setTimeout(() => {
    toast.classList.add("opacity-0", "translate-x-10");
    // Hapus elemen dari DOM setelah animasi selesai
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}
