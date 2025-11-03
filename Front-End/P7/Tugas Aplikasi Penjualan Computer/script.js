document.addEventListener('DOMContentLoaded', () => {
    const elements = {
        btnKategori: document.getElementById('btn-kategori'),
        btnJenisPenjualan: document.getElementById('btn-jenis-penjualan'),
        modalKategori: document.getElementById('modal-kategori'),
        modalBarang: document.getElementById('modal-barang'),
        modalJenisPenjualan: document.getElementById('modal-jenis-penjualan'),
        closeKategori: document.getElementById('close-kategori'),
        closeBarang: document.getElementById('close-barang'),
        closeJenisPenjualan: document.getElementById('close-jenis-penjualan'),
        kategoriOptions: document.querySelectorAll('.kategori-option'),
        jenisPenjualanOptions: document.querySelectorAll('.jenis-penjualan-option'),
        barangList: document.getElementById('barang-list'),
        jumlahInput: document.getElementById('jumlah'),
        kategoriInput: document.getElementById('kategori'),
        jenisPenjualanInput: document.getElementById('jenis-penjualan'),
        namaBarangInput: document.getElementById('nama-barang'),
        hargaSatuanInput: document.getElementById('harga-satuan'),
        hargaSatuanRaw: 0 // Store raw price value
    };

    const requiredElements = [
        'barangList', 'jumlahInput', 'kategoriInput', 
        'jenisPenjualanInput', 'namaBarangInput', 'hargaSatuanInput'
    ];
    
    for (const el of requiredElements) {
        if (!elements[el]) {
            console.error(`Error Handling Aktif, element ${el} tidak ditemukan - ${el}`);
            return;
        }
    }

    const dataBarang = {
        'PC/LAPTOP': [
            { nama: 'PC IBM Core i7', harga: 5600000 },
            { nama: 'Laptop Asus Core i5', harga: 4500000 },
            { nama: 'Laptop Lenovo AMD Ryzen 5', harga: 9500000 }
        ],
        'AKSESORIS': [
            { nama: 'Flashdisk 32gb', harga: 50000 },
            { nama: 'Hardisk 256gb', harga: 1250000 },
            { nama: 'Speaker Aktif', harga: 255000 }
        // ],
        // 'PERIPHARAL': [
        //     { nama: 'Mouse Wireless', harga: 150000 },
        //     { nama: 'Keyboard Mechanical', harga: 350000 },
        //     { nama: 'Monitor 24 inch', harga: 1200000 }
        ]
    };

    elements.btnKategori?.addEventListener('click', () => {
        elements.modalKategori.style.display = 'block';
    });

    elements.btnJenisPenjualan?.addEventListener('click', () => {
        elements.modalJenisPenjualan.style.display = 'block';
    });

    setupModalClose(elements.modalKategori, elements.closeKategori);
    setupModalClose(elements.modalBarang, elements.closeBarang);
    setupModalClose(elements.modalJenisPenjualan, elements.closeJenisPenjualan);

    function setupModalClose(modal, closeBtn) {
        [modal, closeBtn].forEach(el => {
            el?.addEventListener('click', (e) => {
                if (e.target === modal || e.target === closeBtn) {
                    modal.style.display = 'none';
                }
            });
        });
    }

    elements.kategoriOptions.forEach(option => {
        option.addEventListener('click', () => {
            const selectedKategori = option.getAttribute('data-kategori');
            elements.kategoriInput.value = selectedKategori;
            elements.modalKategori.style.display = 'none';
            populateBarang(selectedKategori);
            elements.modalBarang.style.display = 'block';
        });
    });

    elements.jenisPenjualanOptions.forEach(option => {
        option.addEventListener('click', () => {
            const selectedJenis = option.getAttribute('data-jenis');
            elements.jenisPenjualanInput.value = selectedJenis;
            elements.modalJenisPenjualan.style.display = 'none';
            updateTotal();
        });
    });

    function populateBarang(kategori) {
        if (!dataBarang[kategori]) {
            console.error(`Invalid category selected: ${kategori}`);
            return;
        }

        elements.barangList.innerHTML = '';
        dataBarang[kategori].forEach(barang => {
            const button = document.createElement('button');
            button.className = 'barang-option';
            button.innerHTML = `
                <strong>${barang.nama}</strong><br>
                <span class="price">Rp ${formatRupiah(barang.harga)}</span>
            `;
            
            button.addEventListener('click', () => {
                elements.namaBarangInput.value = barang.nama;
                elements.hargaSatuanRaw = barang.harga; // Store raw value
                elements.hargaSatuanInput.value = formatRupiah(barang.harga); // Display formatted value
                elements.modalBarang.style.display = 'none';
                updateTotal();
            });
            elements.barangList.appendChild(button);
        });
    }

    elements.jumlahInput.addEventListener('input', (e) => {
        e.target.value = e.target.value.replace(/[^0-9]/g, '');
        updateTotal();
    });

    function updateTotal() {
        // Use stored raw price value
        const hargaSatuan = elements.hargaSatuanRaw || 0;
        const jumlah = parseInt(elements.jumlahInput.value) || 0;
        const jenisPenjualan = elements.jenisPenjualanInput.value;
        const kategori = elements.kategoriInput.value;

        const totalPenjualan = hargaSatuan * jumlah;
        
        let diskon = 0;
        if (jenisPenjualan === 'Tunai') {
            diskon = totalPenjualan * 0.10;
        }
    
        let pajakPerItem = 0;
        if (kategori === 'PC/LAPTOP') {
            pajakPerItem = hargaSatuan * 0.15;
        } else if (kategori === 'AKSESORIS') {
            pajakPerItem = hargaSatuan * 0.10;
        } else if (kategori === 'PERIPHARAL') {
            pajakPerItem = hargaSatuan * 0.05;
        }
        const pajakTotal = pajakPerItem * jumlah;
        const hargaTotal = (totalPenjualan - diskon) + pajakTotal;
        document.getElementById('total-penjualan').textContent = `Rp ${formatRupiah(totalPenjualan)}`;
        document.getElementById('diskon').textContent = `Rp ${formatRupiah(diskon)}`;
        document.getElementById('pajak').textContent = `Rp ${formatRupiah(pajakTotal)}`;
        document.getElementById('harga-total').textContent = `Rp ${formatRupiah(hargaTotal)}`;
    }
    function formatRupiah(amount) {
        return new Intl.NumberFormat('id-ID', {
            minimumFractionDigits: 0,
            maximumFractionDigits: 0
        }).format(Math.round(amount));
    }
    updateTotal();
});