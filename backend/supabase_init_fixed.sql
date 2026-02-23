-- ============================================
-- FIX: Table names phải khớp với SQLModel
-- Backend dùng: "user", "apartment" (số ít)
-- SQL này tạo đúng table names
-- ============================================

-- Xóa tất cả trước
DROP TABLE IF EXISTS service_bookings CASCADE;
DROP TABLE IF EXISTS services CASCADE;
DROP TABLE IF EXISTS vehicle_registrations CASCADE;
DROP TABLE IF EXISTS ticket_comments CASCADE;
DROP TABLE IF EXISTS tickets CASCADE;
DROP TABLE IF EXISTS notifications CASCADE;
DROP TABLE IF EXISTS payments CASCADE;
DROP TABLE IF EXISTS bills CASCADE;
DROP TABLE IF EXISTS residents CASCADE;
DROP TABLE IF EXISTS apartments CASCADE;
DROP TABLE IF EXISTS apartment CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS "user" CASCADE;
DROP TABLE IF EXISTS price_histories CASCADE;

DROP TYPE IF EXISTS user_role CASCADE;
DROP TYPE IF EXISTS occupier_type CASCADE;
DROP TYPE IF EXISTS apartment_status CASCADE;
DROP TYPE IF EXISTS bill_type CASCADE;
DROP TYPE IF EXISTS bill_status CASCADE;
DROP TYPE IF EXISTS payment_status CASCADE;
DROP TYPE IF EXISTS ticket_status CASCADE;
DROP TYPE IF EXISTS ticket_category CASCADE;
DROP TYPE IF EXISTS ticket_priority CASCADE;
DROP TYPE IF EXISTS vehicle_type CASCADE;
DROP TYPE IF EXISTS vehicle_status CASCADE;
DROP TYPE IF EXISTS service_category CASCADE;
DROP TYPE IF EXISTS service_status CASCADE;
DROP TYPE IF EXISTS booking_status CASCADE;
DROP TYPE IF EXISTS notification_type CASCADE;
DROP TYPE IF EXISTS notification_status CASCADE;
DROP TYPE IF EXISTS price_type CASCADE;

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- CREATE ENUMS (với giá trị đúng theo backend)
-- ============================================
CREATE TYPE user_role AS ENUM ('user', 'manager', 'accountant', 'receptionist');
CREATE TYPE occupier_type AS ENUM ('owner', 'renter');
CREATE TYPE apartment_status AS ENUM ('available', 'occupied', 'maintenance');
CREATE TYPE bill_type AS ENUM ('management_fee', 'utility', 'parking', 'service', 'other');
CREATE TYPE bill_status AS ENUM ('pending', 'paid', 'overdue', 'cancelled');
CREATE TYPE payment_status AS ENUM ('pending', 'completed', 'failed');
CREATE TYPE ticket_status AS ENUM ('open', 'in_progress', 'resolved', 'closed');
CREATE TYPE ticket_category AS ENUM ('maintenance', 'noise', 'cleaning', 'suggestion', 'other');
CREATE TYPE ticket_priority AS ENUM ('low', 'normal', 'high', 'urgent');
CREATE TYPE vehicle_type AS ENUM ('car', 'motorcycle', 'bicycle');
CREATE TYPE vehicle_status AS ENUM ('pending', 'active', 'rejected', 'expired');
CREATE TYPE service_category AS ENUM ('cleaning', 'repair', 'delivery', 'moving', 'other');
CREATE TYPE service_status AS ENUM ('active', 'inactive');
CREATE TYPE booking_status AS ENUM ('pending', 'confirmed', 'completed', 'cancelled');
CREATE TYPE notification_type AS ENUM ('maintenance', 'bill_reminder', 'event', 'announcement', 'system');
CREATE TYPE notification_status AS ENUM ('draft', 'scheduled', 'sent', 'cancelled');
CREATE TYPE price_type AS ENUM ('service', 'management_fee_per_m2', 'parking_car', 'parking_motor', 'parking_bicycle', 'water_tier_1', 'electricity_tier_1', 'other');

-- ============================================
-- CREATE TABLES (với tên đúng: user, apartment)
-- ============================================

-- User table (tên: "user" với quotes vì là reserved keyword)
CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    role user_role DEFAULT 'user',
    apartment_number VARCHAR(20),
    building VARCHAR(10),
    occupier occupier_type DEFAULT 'owner',
    balance DECIMAL(10, 2) DEFAULT 0.00,
    is_active BOOLEAN DEFAULT true,
    reset_otp VARCHAR(10),
    reset_otp_created_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Apartment table (tên: apartment)
CREATE TABLE apartment (
    id SERIAL PRIMARY KEY,
    apartment_number VARCHAR(20) UNIQUE NOT NULL,
    building VARCHAR(10) NOT NULL,
    floor INTEGER NOT NULL,
    area DECIMAL(10, 2) NOT NULL,
    bedrooms INTEGER DEFAULT 1,
    bathrooms INTEGER DEFAULT 1,
    status apartment_status DEFAULT 'available',
    resident_id INTEGER REFERENCES "user"(id) ON DELETE SET NULL,
    description TEXT,
    move_in_date DATE,
    electricity_meter_start DECIMAL(10, 2),
    water_meter_start DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bills table
CREATE TABLE bill (
    id SERIAL PRIMARY KEY,
    bill_number VARCHAR(50) UNIQUE NOT NULL,
    user_id INTEGER REFERENCES "user"(id) ON DELETE CASCADE,
    bill_type bill_type NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    amount DECIMAL(10, 2) NOT NULL,
    due_date TIMESTAMP NOT NULL,
    status bill_status DEFAULT 'pending',
    paid_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tickets table
CREATE TABLE ticket (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES "user"(id) ON DELETE CASCADE,
    category ticket_category NOT NULL,
    priority ticket_priority DEFAULT 'normal',
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    status ticket_status DEFAULT 'open',
    image_url VARCHAR(500),
    assigned_to INTEGER REFERENCES "user"(id) ON DELETE SET NULL,
    resolved_by INTEGER REFERENCES "user"(id) ON DELETE SET NULL,
    resolution_notes TEXT,
    resolved_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Services table
CREATE TABLE service (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    category service_category NOT NULL,
    unit VARCHAR(50) NOT NULL,
    status service_status DEFAULT 'active',
    available_days VARCHAR(50) DEFAULT '[0,1,2,3,4,5,6]',
    available_time_start TIME,
    available_time_end TIME,
    advance_booking_hours INTEGER DEFAULT 24,
    max_booking_days INTEGER DEFAULT 30,
    provider_name VARCHAR(100),
    provider_contact VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Vehicle table
CREATE TABLE vehicle (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES "user"(id) ON DELETE CASCADE,
    vehicle_type vehicle_type NOT NULL,
    license_plate VARCHAR(20) UNIQUE NOT NULL,
    make VARCHAR(50),
    model VARCHAR(50),
    color VARCHAR(30),
    parking_spot VARCHAR(20),
    registration_image VARCHAR(500),
    status vehicle_status DEFAULT 'pending',
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    approved_at TIMESTAMP,
    approved_by INTEGER REFERENCES "user"(id) ON DELETE SET NULL,
    rejection_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Price histories table
CREATE TABLE price_histories (
    id SERIAL PRIMARY KEY,
    type price_type NOT NULL,
    reference_id INTEGER,
    price DECIMAL(10, 2) NOT NULL,
    description VARCHAR(200),
    effective_from TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES "user"(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- CREATE INDEXES
-- ============================================
CREATE INDEX idx_user_username ON "user"(username);
CREATE INDEX idx_user_email ON "user"(email);
CREATE INDEX idx_user_role ON "user"(role);
CREATE INDEX idx_apartment_number ON apartment(apartment_number);
CREATE INDEX idx_apartment_building ON apartment(building);
CREATE INDEX idx_bill_user_id ON bill(user_id);
CREATE INDEX idx_bill_status ON bill(status);
CREATE INDEX idx_ticket_user_id ON ticket(user_id);
CREATE INDEX idx_ticket_status ON ticket(status);
CREATE INDEX idx_vehicle_user_id ON vehicle(user_id);

-- ============================================
-- INSERT ADMIN ACCOUNTS
-- ============================================
INSERT INTO "user" (username, email, hashed_password, full_name, phone, role, balance, occupier) VALUES
('manager', 'manager@apartment.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYG8K8w8Z6G', 'Quản lý hệ thống', '0901234567', 'manager', 0, 'owner'),
('accountant', 'accountant@apartment.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYG8K8w8Z6G', 'Kế toán viên', '0901234568', 'accountant', 0, 'owner'),
('receptionist', 'receptionist@apartment.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYG8K8w8Z6G', 'Lễ tân', '0901234569', 'receptionist', 0, 'owner');

-- ============================================
SELECT 'Database created successfully with correct table names!' as message;
SELECT 'Admin accounts ready - Password: 123456' as info;
SELECT 'Now seed data via API: POST /api/v1/seed/real-data' as next_step;
-- ============================================
