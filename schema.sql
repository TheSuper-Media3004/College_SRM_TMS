-- Create User table if not exists
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(200) NOT NULL,
    name VARCHAR(100) NOT NULL,
    is_admin BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
INSERT OR IGNORE INTO user (email, password, name, is_admin)
VALUES ('admin@college.edu', 'super', 'Admin User', 1);

CREATE TABLE IF NOT EXISTS bus (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bus_number VARCHAR(20) NOT NULL UNIQUE,
    driver_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS route (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    route_number VARCHAR(10) NOT NULL,
    route_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS boarding_point (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stop_number INTEGER NOT NULL,
    location VARCHAR(100) NOT NULL,
    pickup_time TIME NOT NULL,
    route_id INTEGER NOT NULL,
    FOREIGN KEY (route_id) REFERENCES route(id) ON DELETE CASCADE
);

-- Create Student table if not exists
CREATE TABLE IF NOT EXISTS student (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name VARCHAR(100) NOT NULL,
    enrollment_number VARCHAR(20) NOT NULL UNIQUE,
    route_id INTEGER,
    boarding_point_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (route_id) REFERENCES route(id) ON DELETE SET NULL,
    FOREIGN KEY (boarding_point_id) REFERENCES boarding_point(id) ON DELETE SET NULL
);

-- Insert default admin user
INSERT OR IGNORE INTO user (email, password, name, is_admin)
VALUES ('admin@college.edu', 'pbkdf2:sha256:150000$KJrKVgsM$20c76c25677f8a5c69a86569d9b793975c7a3c3633e470d5c5214a0133b71d42', 'Admin User', 1);

-- Insert CET Routes
INSERT OR IGNORE INTO route (route_number, route_name) VALUES ('S1', 'Avadi');
INSERT OR IGNORE INTO route (route_number, route_name) VALUES ('S2', 'Ayanavaram');
INSERT OR IGNORE INTO route (route_number, route_name) VALUES ('S3', 'Koyambedu');
INSERT OR IGNORE INTO route (route_number, route_name) VALUES ('S4', 'Mylapore');
INSERT OR IGNORE INTO route (route_number, route_name) VALUES ('S5', 'Nandambakkam');
INSERT OR IGNORE INTO route (route_number, route_name) VALUES ('S6', 'Thiruvottriyur');
INSERT OR IGNORE INTO route (route_number, route_name) VALUES ('S7', 'Velachery');
INSERT OR IGNORE INTO route (route_number, route_name) VALUES ('S7A', 'Pallikaranai');
INSERT OR IGNORE INTO route (route_number, route_name) VALUES ('S8', 'Mount Subway');
INSERT OR IGNORE INTO route (route_number, route_name) VALUES ('S9', 'Padappai');
INSERT OR IGNORE INTO route (route_number, route_name) VALUES ('S10', 'Chengalpat');
INSERT OR IGNORE INTO route (route_number, route_name) VALUES ('S11', 'Chrompet');
INSERT OR IGNORE INTO route (route_number, route_name) VALUES ('S12', 'Senthil Nagar');

-- Insert Boarding Points for S1 (Avadi)
INSERT OR IGNORE INTO boarding_point (stop_number, location, pickup_time, route_id)
SELECT 1, 'Avadi', '06:20:00', id FROM route WHERE route_number = 'S1';
INSERT OR IGNORE INTO boarding_point (stop_number, location, pickup_time, route_id)
SELECT 2, 'Thirumullaivoyal', '06:27:00', id FROM route WHERE route_number = 'S1';
INSERT OR IGNORE INTO boarding_point (stop_number, location, pickup_time, route_id)
SELECT 3, 'Ambattur OT', '06:35:00', id FROM route WHERE route_number = 'S1';
INSERT OR IGNORE INTO boarding_point (stop_number, location, pickup_time, route_id)
SELECT 4, 'Decathlon Service road', '06:45:00', id FROM route WHERE route_number = 'S1';
INSERT OR IGNORE INTO boarding_point (stop_number, location, pickup_time, route_id)
SELECT 5, 'Porur Toll Gate', '06:55:00', id FROM route WHERE route_number = 'S1';

-- Insert Boarding Points for S2 (Ayanavaram)
INSERT OR IGNORE INTO boarding_point (stop_number, location, pickup_time, route_id)
SELECT 1, 'Kellys', '06:05:00', id FROM route WHERE route_number = 'S2';
INSERT OR IGNORE INTO boarding_point (stop_number, location, pickup_time, route_id)
SELECT 2, 'Mental Hospital (Keezhpak)', '06:10:00', id FROM route WHERE route_number = 'S2';
INSERT OR IGNORE INTO boarding_point (stop_number, location, pickup_time, route_id)
SELECT 3, 'Ayanavaram Singnal', '06:12:00', id FROM route WHERE route_number = 'S2';
INSERT OR IGNORE INTO boarding_point (stop_number, location, pickup_time, route_id)
SELECT 4, 'Noor Hotel', '06:15:00', id FROM route WHERE route_number = 'S2';
INSERT OR IGNORE INTO boarding_point (stop_number, location, pickup_time, route_id)
SELECT 5, 'Joint Office', '06:20:00', id FROM route WHERE route_number = 'S2';
INSERT OR IGNORE INTO boarding_point (stop_number, location, pickup_time, route_id)
SELECT 6, 'Pollice Quatras', '06:22:00', id FROM route WHERE route_number = 'S2';
INSERT OR IGNORE INTO boarding_point (stop_number, location, pickup_time, route_id)
SELECT 7, 'ICF', '06:25:00', id FROM route WHERE route_number = 'S2';
INSERT OR IGNORE INTO boarding_point (stop_number, location, pickup_time, route_id)
SELECT 8, 'Nathamuni', '06:30:00', id FROM route WHERE route_number = 'S2';
INSERT OR IGNORE INTO boarding_point (stop_number, location, pickup_time, route_id)
SELECT 9, 'Anna Nagar West Depot', '06:35:00', id FROM route WHERE route_number = 'S2';
INSERT OR IGNORE INTO boarding_point (stop_number, location, pickup_time, route_id)
SELECT 10, 'Rohini Theatre', '06:40:00', id FROM route WHERE route_number = 'S2';
INSERT OR IGNORE INTO boarding_point (stop_number, location, pickup_time, route_id)
SELECT 11, 'Madhuravoyal Erikarai', '06:50:00', id FROM route WHERE route_number = 'S2';

-- Insert Boarding Points for S3 (Koyambedu)
INSERT OR IGNORE INTO boarding_point (stop_number, location, pickup_time, route_id)
SELECT 1, 'Koyambedu', '06:15:00', id FROM route WHERE route_number = 'S3';
INSERT OR IGNORE INTO boarding_point (stop_number, location, pickup_time, route_id)
SELECT 2, 'MMDA', '06:20:00', id FROM route WHERE route_number = 'S3';
INSERT OR IGNORE INTO boarding_point (stop_number, location, pickup_time, route_id)
SELECT 3, 'Vadapalani', '06:25:00', id FROM route WHERE route_number = 'S3';
INSERT OR IGNORE INTO boarding_point (stop_number, location, pickup_time, route_id)
SELECT 4, 'Ashok Pillar', '06:29:00', id FROM route WHERE route_number = 'S3';
INSERT OR IGNORE INTO boarding_point (stop_number, location, pickup_time, route_id)
SELECT 5, 'Kasi Theatre', '06:32:00', id FROM route WHERE route_number = 'S3';
INSERT OR IGNORE INTO boarding_point (stop_number, location, pickup_time, route_id)
SELECT 6, 'Ekkattuthangal', '06:35:00', id FROM route WHERE route_number = 'S3';
INSERT OR IGNORE INTO boarding_point (stop_number, location, pickup_time, route_id)
SELECT 7, 'Pallavaram', '06:50:00', id FROM route WHERE route_number = 'S3';
INSERT OR IGNORE INTO boarding_point (stop_number, location, pickup_time, route_id)
SELECT 8, 'MIT Chrompet', '07:00:00', id FROM route WHERE route_number = 'S3';

-- Insert Boarding Points for S4 (Mylapore)
INSERT OR IGNORE INTO boarding_point (stop_number, location, pickup_time, route_id)
SELECT 1, 'Mylapore Tank', '06:15:00', id FROM route WHERE route_number = 'S4';
INSERT OR IGNORE INTO boarding_point (stop_number, location, pickup_time, route_id)
SELECT 2, 'Mandeveli Depot', '06:17:00', id FROM route WHERE route_number = 'S4';
INSERT OR IGNORE INTO boarding_point (stop_number, location, pickup_time, route_id)
SELECT 3, 'Vannandurai', '06:27:00', id FROM route WHERE route_number = 'S4';
INSERT OR IGNORE INTO boarding_point (stop_number, location, pickup_time, route_id)
SELECT 4, 'Indira Nagar Watter Tank', '06:30:00', id FROM route WHERE route_number = 'S4';
INSERT OR IGNORE INTO boarding_point (stop_number, location, pickup_time, route_id)
SELECT 5, 'Adayar Canal', '06:32:00', id FROM route WHERE route_number = 'S4';
INSERT OR IGNORE INTO boarding_point (stop_number, location, pickup_time, route_id)
SELECT 6, 'IIT', '06:35:00', id FROM route WHERE route_number = 'S4';
INSERT OR IGNORE INTO boarding_point (stop_number, location, pickup_time, route_id)
SELECT 7, 'Anna Univercity', '06:37:00', id FROM route WHERE route_number = 'S4';
INSERT OR IGNORE INTO boarding_point (stop_number, location, pickup_time, route_id)
SELECT 8, 'Guindy', '06:40:00', id FROM route WHERE route_number = 'S4';
INSERT OR IGNORE INTO boarding_point (stop_number, location, pickup_time, route_id)
SELECT 9, 'Chrompet', '07:10:00', id FROM route WHERE route_number = 'S4';
