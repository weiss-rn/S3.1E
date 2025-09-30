var ulangi = confirm("Apakah anda ingin mengulang?");
var counter = 0;

while (ulangi) {
    alert("Perulangan ke-" + counter);
    counter++;
    ulangi = confirm("Apakah anda ingin mengulang?");
}

alert("Perulangan selesai dan dilakukan sebanyak" + counter + "kali");
