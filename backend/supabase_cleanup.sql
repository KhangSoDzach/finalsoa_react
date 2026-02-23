-- ============================================
-- CLEANUP SCRIPT - Xóa tất cả để chạy lại từ đầu
-- Chạy script này TRƯỚC KHI chạy supabase_init.sql
-- ============================================

-- Step 1: Drop all tables (with CASCADE to remove dependencies)
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
DROP TABLE IF EXISTS apartment CASCADE;  -- Thử cả tên số ít
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS "user" CASCADE;  -- Thử cả tên số ít với quotes
DROP TABLE IF EXISTS price_histories CASCADE;
DROP TABLE IF EXISTS price_history CASCADE;  -- Thử cả tên số ít

-- Step 2: Drop all ENUMs (with CASCADE to remove dependencies)
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

-- Step 3: Drop any other objects that might exist
DROP SCHEMA IF EXISTS public CASCADE;
CREATE SCHEMA public;

-- Step 4: Re-enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
SELECT 'Database cleaned successfully! Now run supabase_init.sql' as message;
-- ============================================
