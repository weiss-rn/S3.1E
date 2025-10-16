document.addEventListener("DOMContentLoaded", function() {
    const prices = {
        "Honda": 20000000,
        "Yamaha": 18000000,
        "Suzuki": 15000000,
        "Helm": 500000,
        "Jaket": 300000,
        "Velg": 1000000
    };

    const motorSelect = document.getElementById("motor");
    const helmCheckbox = document.getElementById("eq1");
    const jaketCheckbox = document.getElementById("eq2");
    const velgCheckbox = document.getElementById("eq3");
    const pembayaranRadios = document.querySelectorAll('input[name="pembayaran"]');
    const hargaInput = document.getElementById("harga");
    const bungaDiskonInput = document.getElementById("bunga_diskon");
    const totalInput = document.getElementById("total");
    const prosesButton = document.getElementById("btn-submit");
    const resetButton = document.getElementById("btn-reset");

    function calculateTotal() {
        const motor = motorSelect.value;
        const isHelm = helmCheckbox.checked;
        const isJaket = jaketCheckbox.checked;
        const isVelg = velgCheckbox.checked;
        const pembayaran = document.querySelector('input[name="pembayaran"]:checked');

        let harga = 0;
        if (motor && prices[motor]) {
            harga += prices[motor];
        }

        if (isHelm) harga += prices["Helm"];
        if (isJaket) harga += prices["Jaket"];
        if (isVelg) harga += prices["Velg"];

        let bungaDiskon = 0;
        let total = harga;

        if (pembayaran) {
            if (pembayaran.value === "tunai") {
                bungaDiskon = harga * 0.1; // 10% kalau tunai
                total = harga - bungaDiskon;
            } else if (pembayaran.value === "kredit") {
                bungaDiskon = harga * 0.15; // 15% kalo kredit
                total = harga + bungaDiskon;
            }
        }

        hargaInput.value = formatRupiah(harga);
        bungaDiskonInput.value = formatRupiah(bungaDiskon);
        totalInput.value = formatRupiah(total);
    }

    function formatRupiah(angka) {
        if (angka === 0) return "Rp 0";
        var number_string = angka.toString().replace(/[^,\d]/g, ''),
            split = number_string.split(','),
            sisa = split[0].length % 3,
            rupiah = split[0].substr(0, sisa),
            ribuan = split[0].substr(sisa).match(/\d{3}/gi);

        if (ribuan) {
            separator = sisa ? '.' : '';
            rupiah += separator + ribuan.join('.');
        }

        rupiah = split[1] != undefined ? rupiah + ',' + split[1] : rupiah;
        return 'Rp ' + rupiah;
    }
    
    function resetForm() {
        document.getElementById("form-penjualan").reset();
        hargaInput.value = "";
        bungaDiskonInput.value = "";
        totalInput.value = "";
    }

    prosesButton.addEventListener("click", calculateTotal);
    resetButton.addEventListener("click", resetForm);

    motorSelect.addEventListener("change", calculateTotal);
    helmCheckbox.addEventListener("change", calculateTotal);
    jaketCheckbox.addEventListener("change", calculateTotal);
    velgCheckbox.addEventListener("change", calculateTotal);
    pembayaranRadios.forEach(radio => {
        radio.addEventListener("change", calculateTotal);
    });
});