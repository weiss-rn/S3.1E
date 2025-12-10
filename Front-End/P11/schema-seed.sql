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
('USB-C Cable 1m', 'Kabel USB-C braided panjang 1 meter.', 49000.00, 'cable.jpg'),
('Monitor 27" 144Hz', 'Monitor gaming dengan refresh rate 144Hz dan response time 1ms.', 2499000.00, 'monitor.jpg'),
('Webcam 4K', 'Webcam USB 4K dengan autofocus dan built-in microphone.', 879000.00, 'webcam.jpg'),
('Mousepad XXL', 'Mousepad besar 800x300mm dengan base non-slip.', 129000.00, 'mousepad.jpg'),
('USB Hub 7-Port', 'Hub USB 3.0 dengan 7 port dan power adapter 4A.', 349000.00, 'usbhub.jpg'),
('Screen Protector Set', 'Paket 3 screen protector tempered glass anti-glare.', 99000.00, 'screenprotector.jpg'),
('Laptop Stand Aluminium', 'Stand laptop adjustable ergonomis dari aluminium.', 299000.00, 'laptopad.jpg');
