-- P11-Proxy (MySQL) schema + example data
-- Usage:
--   1) Create/select your DB (example: USE testdb;)
--   2) Run this file in MySQL/MariaDB client.

CREATE TABLE IF NOT EXISTS barang (
    id INT AUTO_INCREMENT PRIMARY KEY,
    kode VARCHAR(50) NOT NULL,
    nama VARCHAR(100) NOT NULL,
    harga DECIMAL(12, 2) NOT NULL,
    gambar VARCHAR(255),
    jumlah INT NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO barang (kode, nama, harga, gambar, jumlah) VALUES
('BRG001', 'Kopi Bubuk 250g', 45000.00, NULL, 25),
('BRG002', 'Keripik Pisang', 15000.00, 'Screenshot_2025-12-10_111853.png', 40),
('BRG003', 'Sambal Botol 200ml', 28000.00, NULL, 12),
('BRG004', 'Teh Herbal', 35000.00, NULL, 18),
('BRG005', 'Sabun Handmade', 22000.00, NULL, 30),
('BRG006', 'Madu 500ml', 85000.00, NULL, 7);

