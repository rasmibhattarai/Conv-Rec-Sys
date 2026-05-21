CREATE TABLE washing_machines (
    id INTEGER PRIMARY KEY,
    name TEXT,
    brand TEXT,
    type TEXT,
    size TEXT,
    price INTEGER,
    color TEXT,
    warranty TEXT,
    energy_rating TEXT,
    features TEXT
);

CREATE TABLE fridges (
    id INTEGER PRIMARY KEY,
    name TEXT,
    brand TEXT,
    type TEXT,
    size TEXT,
    price INTEGER,
    color TEXT,
    warranty TEXT,
    energy_rating TEXT,
    features TEXT
);

CREATE TABLE tvs (
    id INTEGER PRIMARY KEY,
    name TEXT,
    brand TEXT,
    type TEXT,
    size TEXT,
    price INTEGER,
    color TEXT,
    warranty TEXT,
    resolution TEXT,
    features TEXT
);

CREATE TABLE dishwashers (
    id INTEGER PRIMARY KEY,
    name TEXT,
    brand TEXT,
    type TEXT,
    size TEXT,
    price INTEGER,
    color TEXT,
    warranty TEXT,
    energy_rating TEXT,
    features TEXT
);

INSERT INTO washing_machines (id, name, brand, type, size, price, color, warranty, energy_rating, features) VALUES 
(1, 'WM-Pro-800', 'LG', 'Front Load', '8kg', 450, 'Silver', '2 years', 'A+++', 'Inverter, Steam'),
(2, 'WM-Eco-700', 'Samsung', 'Top Load', '7kg', 350, 'White', '1 year', 'A++', 'Digital Display'),
(3, 'WM-Max-900', 'LG', 'Front Load', '9kg', 550, 'Silver', '2 years', 'A+++', 'AI Wash, Steam'),
(4, 'WM-Smart-8', 'Samsung', 'Front Load', '8kg', 500, 'Black', '2 years', 'A+++', 'WiFi, Inverter'),
(5, 'WM-Basic-7', 'LG', 'Top Load', '7kg', 300, 'White', '1 year', 'A+', 'Quick Wash'),
(6, 'WM-Premium-10', 'Samsung', 'Front Load', '10kg', 700, 'Silver', '3 years', 'A+++', 'AI, Steam, WiFi'),
(7, 'WM-Compact-6', 'LG', 'Top Load', '6kg', 280, 'Blue', '1 year', 'A++', 'Space Save'),
(8, 'WM-Deluxe-9', 'Samsung', 'Front Load', '9kg', 600, 'Black', '2 years', 'A+++', 'Hygiene Steam'),
(9, 'WM-Standard-8', 'LG', 'Front Load', '8kg', 400, 'Silver', '2 years', 'A++', 'Inverter'),
(10, 'WM-Elite-10', 'Samsung', 'Front Load', '10kg', 750, 'Silver', '3 years', 'A+++', 'Smart Diagnosis');

INSERT INTO fridges (id, name, brand, type, size, price, color, warranty, energy_rating, features) VALUES 
(1, 'RF-Double-300', 'LG', 'Double Door', '300L', 550, 'Silver', '2 years', 'A++', 'Frost Free'),
(2, 'RF-Single-200', 'Samsung', 'Single Door', '200L', 350, 'White', '1 year', 'A+', 'Direct Cool'),
(3, 'RF-Side-500', 'LG', 'Side-by-Side', '500L', 900, 'Black', '2 years', 'A+++', 'Ice Maker'),
(4, 'RF-Triple-400', 'Samsung', 'Triple Door', '400L', 700, 'Silver', '2 years', 'A++', 'Convertible'),
(5, 'RF-Compact-150', 'LG', 'Single Door', '150L', 250, 'Red', '1 year', 'A', 'Mini Bar'),
(6, 'RF-Family-450', 'Samsung', 'Double Door', '450L', 750, 'Black', '3 years', 'A+++', 'Smart Inverter'),
(7, 'RF-Retro-250', 'LG', 'Single Door', '250L', 400, 'Blue', '2 years', 'A+', 'Retro Design'),
(8, 'RF-Luxury-600', 'Samsung', 'Side-by-Side', '600L', 1200, 'Silver', '3 years', 'A+++', 'WiFi, Camera'),
(9, 'RF-Standard-350', 'LG', 'Double Door', '350L', 600, 'White', '2 years', 'A++', 'Multi Flow'),
(10, 'RF-Eco-300', 'Samsung', 'Double Door', '300L', 500, 'Silver', '2 years', 'A++', 'Digital Inverter');

INSERT INTO tvs (id, name, brand, type, size, price, color, warranty, resolution, features) VALUES 
(1, 'TV-Smart-40', 'LG', 'LED', '40"', 350, 'Black', '2 years', '4K', 'WebOS, HDR'),
(2, 'TV-OLED-55', 'Samsung', 'OLED', '55"', 900, 'Black', '2 years', '4K', 'Smart Hub'),
(3, 'TV-QLED-65', 'LG', 'QLED', '65"', 1100, 'Silver', '3 years', '4K', 'AI Picture'),
(4, 'TV-LED-32', 'Samsung', 'LED', '32"', 200, 'Black', '1 year', 'HD', 'Tizen OS'),
(5, 'TV-UHD-50', 'LG', 'LED', '50"', 500, 'Black', '2 years', '4K', 'ThinQ AI'),
(6, 'TV-Premium-75', 'Samsung', 'QLED', '75"', 1800, 'Silver', '3 years', '8K', 'Object Sound'),
(7, 'TV-Basic-40', 'LG', 'LED', '40"', 300, 'Black', '1 year', 'Full HD', 'Simple Remote'),
(8, 'TV-Gaming-55', 'Samsung', 'LED', '55"', 650, 'Black', '2 years', '4K', '120Hz, VRR'),
(9, 'TV-Cinema-65', 'LG', 'OLED', '65"', 1400, 'Black', '3 years', '4K', 'Dolby Vision'),
(10, 'TV-Standard-43', 'Samsung', 'LED', '43"', 400, 'Silver', '2 years', '4K', 'Smart TV');

INSERT INTO dishwashers (id, name, brand, type, size, price, color, warranty, energy_rating, features) VALUES 
(1, 'DW-Built-12', 'LG', 'Built-in', '12 place', 450, 'Silver', '2 years', 'A++', 'Quiet 44dB'),
(2, 'DW-Freest-14', 'Samsung', 'Freestanding', '14 place', 550, 'Black', '2 years', 'A+++', 'Zone Wash'),
(3, 'DW-Compact-6', 'LG', 'Compact', '6 place', 300, 'White', '1 year', 'A+', 'Tabletop'),
(4, 'DW-Premium-15', 'Samsung', 'Built-in', '15 place', 700, 'Silver', '3 years', 'A+++', 'WiFi, Steam'),
(5, 'DW-Standard-12', 'LG', 'Freestanding', '12 place', 400, 'Silver', '2 years', 'A++', 'Turbo Dry'),
(6, 'DW-Smart-14', 'Samsung', 'Built-in', '14 place', 600, 'Black', '2 years', 'A+++', 'Auto Open'),
(7, 'DW-Eco-10', 'LG', 'Freestanding', '10 place', 350, 'White', '1 year', 'A+', 'Eco Mode'),
(8, 'DW-Luxury-16', 'Samsung', 'Built-in', '16 place', 850, 'Silver', '3 years', 'A+++', 'AI Wash'),
(9, 'DW-Quick-12', 'LG', 'Freestanding', '12 place', 420, 'Black', '2 years', 'A++', '30min Wash'),
(10, 'DW-Basic-8', 'Samsung', 'Compact', '8 place', 280, 'White', '1 year', 'A', 'Half Load');