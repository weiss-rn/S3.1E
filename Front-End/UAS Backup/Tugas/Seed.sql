-- InnoDB MySQL Data Seeding - ready to inject into the `products` table 

CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    image VARCHAR(255),
    INDEX idx_products_category (category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO products (name, category, description, price, image) VALUES
('Oli Mesin 10W-40 (1L)', 'oli', 'Oli mesin semi-sintetik 10W-40 untuk motor harian. Membantu menjaga performa dan suhu mesin.', 65000.00, 'Mesin10w40.webp'),
('Oli Sintetik 10W-40 (1L)', 'oli', 'Oli full sintetik untuk proteksi maksimal pada mesin berputaran tinggi.', 98000.00, 'sintetik10w40.jpg'),
('Filter Oli Motor', 'oli', 'Filter oli kompatibel untuk berbagai tipe motor (cek kecocokan sebelum membeli).', 25000.00, 'filter_oli.jpg'),
('Busi Iridium', 'kelistrikan', 'Busi iridium untuk pengapian stabil, akselerasi lebih responsif, dan umur pakai lebih panjang.', 45000.00, 'busi_iridium.webp'),
('Kampas Rem Depan', 'rem', 'Kampas rem depan material komposit, pengereman lebih pakem dan minim bunyi.', 75000.00, 'kampas_depan.jpg'),
('Kampas Rem Belakang', 'rem', 'Kampas rem belakang tahan panas untuk pemakaian harian dan touring.', 70000.00, 'kampas_belakang.jpg'),
('Rantai + Gear Set', 'rantai', 'Satu set rantai dan gear untuk akselerasi halus; cocok untuk upgrade/servis berkala.', 285000.00, 'Mesin10w40.webp'),
('Aki Kering MF', 'kelistrikan', 'Aki kering maintenance free, siap pakai, daya starter stabil.', 215000.00, 'akimf.jpg'),
('Ban Tubeless 80/90-14', 'ban', 'Ban tubeless untuk skutik, grip bagus di kondisi kering/basah.', 245000.00, 'tubeless.jpg'),
('Lampu LED Headlamp', 'kelistrikan', 'Lampu LED terang dan hemat daya untuk headlamp motor (12V).', 120000.00, 'hdlamp.jpg'),
('Shockbreaker Belakang', 'mesin', 'Shockbreaker belakang dengan redaman nyaman untuk jalanan kota.', 325000.00, 'sbreakerimages.jpg'),
('Kabel Gas', 'mesin', 'Kabel gas pengganti, tarikan lebih ringan dan responsif.', 35000.00, 'kabelimages.jpg');
