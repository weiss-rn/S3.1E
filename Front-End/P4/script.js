var dataBarang = [
    { name: "Buku Tulis", quantity: 1, price: 5000 },
    { name: "Pensil", quantity: 2, price: 2000 },
    { name: "Spidol", quantity: 1, price: 4000 }
];

function formatCurrency(n) {
    return Number(n).toLocaleString();
}

function showBarang() {
    var listBarang = document.getElementById("list");
    listBarang.innerHTML = "";
    for (let i = 0; i < dataBarang.length; i++) {
        var item = dataBarang[i];
        var btnEdit = "<a href='#' onclick='editBarang(" + i + ")'>Edit</a>";
        var btnHapus = "<a href='#' onclick='deleteBarang(" + i + ")'>Hapus</a>";

        var total = Number(item.quantity) * Number(item.price);
        listBarang.innerHTML += "<li>" +
            "<strong>" + item.name + "</strong> — " +
            "Qty: " + item.quantity + " | " +
            "Price: " + formatCurrency(item.price) + " | " +
            "Total: " + formatCurrency(total) +
            " [" + btnEdit + " | " + btnHapus + "]" +
            "</li>";
    }
}

function addBarang() {
    var inputName = document.querySelector("#item");
    var inputQty = document.querySelector("#quantity");
    var inputPrice = document.querySelector("#price");

    var name = inputName.value && inputName.value.trim();
    var qty = Number(inputQty.value);
    var price = Number(inputPrice.value);

    if (!name) {
        return showBarang();
    }

    if (!Number.isFinite(qty) || qty <= 0) qty = 1;
    if (!Number.isFinite(price) || price < 0) price = 0;

    dataBarang.push({ name: name, quantity: qty, price: price });

    inputName.value = "";
    inputQty.value = "";
    inputPrice.value = "";

    showBarang();
}

function editBarang(id) {
    var item = dataBarang[id];
    if (!item) return;

    var newName = prompt("Nama baru", item.name);
    if (newName === null) return;
    newName = newName.trim();
    if (newName.length === 0) newName = item.name;

    var newQtyStr = prompt("Jumlah (quantity)", String(item.quantity));
    if (newQtyStr === null) return;
    var newQty = Number(newQtyStr);
    if (!Number.isFinite(newQty) || newQty <= 0) newQty = item.quantity;

    var newPriceStr = prompt("Harga (price)", String(item.price));
    if (newPriceStr === null) return;
    var newPrice = Number(newPriceStr);
    if (!Number.isFinite(newPrice) || newPrice < 0) newPrice = item.price;

    dataBarang[id] = { name: newName, quantity: newQty, price: newPrice };
    showBarang();
}

function deleteBarang(id) {
    dataBarang.splice(id, 1);
    showBarang();
}

showBarang();