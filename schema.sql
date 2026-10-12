-- ==========================================================
-- Costume Rental System - Full Database Schema (ไฟล์รวมฉบับส่ง)
-- ==========================================================
-- ระบบจัดการร้านเช่าชุด (3NF Database Architecture)
-- โครงสร้างตาราง: Categories, Customers, Costumes, Rentals
-- ไม่รวม seed data (โครงสร้างล้วนสำหรับนำไป Import)
-- ==========================================================
-- วิธีใช้: นำเข้าผ่านเครื่องมือจัดการฐานข้อมูล (เช่น SQLite / phpMyAdmin)
-- รองรับการรันซ้ำอย่างปลอดภัย (ใช้คำสั่ง IF NOT EXISTS)
-- ==========================================================

-- ==========================
-- 1) CATEGORIES (ประเภทชุด)
-- ==========================
create table if not exists categories (
    category_id integer primary key autoincrement,
    category_name text not null
);

-- ==========================
-- 2) CUSTOMERS (ข้อมูลลูกค้า)
-- ==========================
create table if not exists customers (
    customer_id integer primary key autoincrement,
    customer_name text not null,
    phone text,
    address text
);

-- ==========================
-- 3) COSTUMES (ข้อมูลชุดในร้าน)
-- ==========================
create table if not exists costumes (
    costume_id integer primary key autoincrement,
    category_id integer not null,
    costume_name text not null,
    size text,
    rental_price real not null,
    status text default 'พร้อมใช้งาน',
    foreign key (category_id) references categories(category_id)
);

-- ==========================
-- 4) RENTALS (รายการเช่า-คืน)
-- ==========================
create table if not exists rentals (
    rental_id integer primary key autoincrement,
    customer_id integer not null,
    costume_id integer not null,
    rental_date text not null,
    return_date text not null,
    status text default 'กำลังเช่า',
    foreign key (customer_id) references customers(customer_id),
    foreign key (costume_id) references costumes(costume_id)
);