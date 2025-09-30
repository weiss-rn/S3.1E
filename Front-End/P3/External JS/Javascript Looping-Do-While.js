var ulangi = confirm("Apakah anda ingin mengulangi?");
var counter = 0;
do {
    alert("Perulangan ke-" + counter);
    counter++;
} while (ulangi);
counter++;
alert("Perulangan ke-" + counter);
document.write("Perulangan ke-" + counter);
