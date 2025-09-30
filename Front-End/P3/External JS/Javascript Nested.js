var username = prompt("Masukkan username Anda:");
var password = prompt("Masukkan password Anda:");

if (username === "admin" && password === "password") {
    alert("Selamat datang, admin!");
} else if (username === "user" && password === "password") {
    alert("Selamat datang, user!");
} else {
    alert("Username atau password salah. Silakan coba lagi.");
}
