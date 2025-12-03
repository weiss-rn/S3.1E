CREATE TABLE IF NOT EXISTS stok (
    id INT AUTO_INCREMENT PRIMARY KEY,
    kode_sparepart VARCHAR(50) NOT NULL,
    nama_sparepart VARCHAR(100) NOT NULL,
    harga DECIMAL(10, 2) NOT NULL,
    stok INT NOT NULL,
    tipe_motor VARCHAR(100),
    image VARCHAR(255)
);