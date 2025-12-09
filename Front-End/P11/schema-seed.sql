-- Example data for the mobile ecommerce app
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    image VARCHAR(255)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO products (name, description, price, image) VALUES
('Headphone Bluetooth', 'Headphone wireless ringan dengan baterai 20 jam.', 299000.00, 'headphone.jpg'),
('Mouse Wireless', 'Mouse ergonomis 2.4G dengan DPI adjustable.', 159000.00, 'mouse.jpg'),
('Keyboard Mekanik', 'Keyboard mekanik 87-key switch biru dengan backlight.', 549000.00, 'keyboard.jpg'),
('Charger 30W', 'Charger cepat USB-C 30W kompatibel dengan banyak perangkat.', 189000.00, 'charger.jpg'),
('Powerbank 10.000mAh', 'Powerbank tipis dengan dua port output.', 249000.00, 'powerbank.jpg'),
('USB-C Cable 1m', 'Kabel USB-C braided panjang 1 meter.', 49000.00, 'cable.jpg');
z