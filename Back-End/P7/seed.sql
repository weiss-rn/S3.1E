CREATE TABLE IF NOT EXISTS stok (
    id INT AUTO_INCREMENT PRIMARY KEY,
    kode_sparepart VARCHAR(50) NOT NULL,
    nama_sparepart VARCHAR(100) NOT NULL,
    harga DECIMAL(10, 2) NOT NULL,
    stok INT NOT NULL,
    tipe_motor VARCHAR(100),
    image VARCHAR(255)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


INSERT INTO stok (kode_sparepart, nama_sparepart, harga, stok, tipe_motor, image) VALUES
('SP001', 'Ban Depan Honda Beat', 150000.00, 10, 'Honda Beat', NULL),
('SP002', 'Ban Belakang Yamaha Mio', 180000.00, 8, 'Yamaha Mio', NULL),
('SP003', 'Oli Mesin Suzuki Satria', 25000.00, 20, 'Suzuki Satria', NULL),
('SP004', 'Busi Kawasaki Ninja', 15000.00, 30, 'Kawasaki Ninja', NULL),
('SP005', 'Filter Udara Honda Vario', 35000.00, 15, 'Honda Vario', NULL),
('SP006', 'Rantai Yamaha Aerox', 75000.00, 12, 'Yamaha Aerox', NULL),
('SP007', 'Kampas Rem Depan Suzuki Smash', 50000.00, 25, 'Suzuki Smash', NULL),
('SP008', 'Kampas Rem Belakang Kawasaki W175', 55000.00, 22, 'Kawasaki W175', NULL),
('SP009', 'Bohlam Honda Revo', 10000.00, 40, 'Honda Revo', NULL),
('SP010', 'Aki Yamaha Jupiter', 200000.00, 5, 'Yamaha Jupiter', NULL),
('SP011', 'Velg Racing', 450000.00, 7, 'Universal', NULL),
('SP012', 'Knalpot Racing', 350000.00, 6, 'Universal', NULL),
('SP013', 'Shockbreaker Depan', 250000.00, 9, 'Universal', NULL),
('SP014', 'Shockbreaker Belakang', 275000.00, 8, 'Universal', NULL),

('SP015', 'Lampu Sein LED', 25000.00, 35, 'Universal', NULL);
