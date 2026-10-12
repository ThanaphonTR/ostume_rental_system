import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# =========================
# สร้างและเชื่อมต่อ Database
# =========================
def connect_db():
    return sqlite3.connect("costume_rental.db")

def init_db():
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS costumes (
            costume_id INTEGER PRIMARY KEY AUTOINCREMENT,
            costume_name TEXT NOT NULL,
            category_id INTEGER,
            size TEXT,
            rental_price REAL,
            status TEXT,
            FOREIGN KEY (category_id) REFERENCES categories(category_id)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            phone TEXT,
            address TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rentals (
            rental_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            costume_id INTEGER,
            rental_date TEXT,
            return_date TEXT,
            status TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
            FOREIGN KEY (costume_id) REFERENCES costumes(costume_id)
        )
    """)
    
    # ข้อมูลเริ่มต้น (Demo Data)
    cursor.execute("SELECT COUNT(*) FROM categories")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO categories (category_name) VALUES (?)", [
            ("ชุดไทย",), ("ชุดราตรี",), ("ชุดแฟนซี",), ("ชุดสูทสากล",)
        ])
        
    cursor.execute("SELECT COUNT(*) FROM costumes")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO costumes (costume_name, category_id, size, rental_price, status) VALUES (?, ?, ?, ?, ?)", [
            ("ชุดไทยประยุกต์", 1, "M", 500, "พร้อมใช้งาน"),
            ("ชุดราตรีสั้นสีแดง", 2, "S", 700, "กำลังเช่า"),
            ("ชุดซูเปอร์ฮีโร่", 3, "L", 450, "พร้อมใช้งาน"),
            ("ชุดสูททาซิโด้", 4, "XL", 800, "พร้อมใช้งาน")
        ])
        
    cursor.execute("SELECT COUNT(*) FROM customers")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO customers (customer_name, phone, address) VALUES (?, ?, ?)", [
            ("สมชาย ใจดี", "081-234-5678", "เชียงใหม่"),
            ("สมหญิง รักงาม", "089-876-5432", "พะเยา")
        ])

    conn.commit()
    conn.close()

init_db()


# =========================
# หน้าต่างจัดการชุด (เพิ่มชุดได้จริง)
# =========================
def show_costumes():
    window = tk.Toplevel(root)
    window.title("จัดการชุดเดโม")
    window.geometry("900x520")

    title = tk.Label(window, text="👗 ระบบจัดการชุด", font=("Arial", 18, "bold"))
    title.pack(pady=10)

    # กรอบฟอร์มเพิ่มข้อมูล
    form_frame = tk.LabelFrame(window, text=" เพิ่มข้อมูลชุดใหม่ ", font=("Arial", 11, "bold"), padx=10, pady=10)
    form_frame.pack(fill="x", padx=20, pady=5)

    tk.Label(form_frame, text="ชื่อชุด:").grid(row=0, column=0, sticky="w", padx=5)
    e_name = tk.Entry(form_frame, width=18)
    e_name.grid(row=0, column=1, padx=5)

    tk.Label(form_frame, text="ประเภท (1:ไทย, 2:ราตรี, 3:แฟนซี, 4:สูท):").grid(row=0, column=2, sticky="w", padx=5)
    e_cat = tk.Entry(form_frame, width=8)
    e_cat.grid(row=0, column=3, padx=5)
    e_cat.insert(0, "1")

    tk.Label(form_frame, text="ไซซ์:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    e_size = tk.Entry(form_frame, width=18)
    e_size.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="ราคาเช่า:").grid(row=1, column=2, sticky="w", padx=5, pady=5)
    e_price = tk.Entry(form_frame, width=8)
    e_price.grid(row=1, column=3, padx=5, pady=5)

    # ตารางแสดงผล
    table = ttk.Treeview(window, columns=("id", "name", "category", "size", "price", "status"), show="headings")
    table.heading("id", text="รหัส")
    table.heading("name", text="ชื่อชุด")
    table.heading("category", text="ประเภท")
    table.heading("size", text="ไซซ์")
    table.heading("price", text="ราคาเช่า (บาท)")
    table.heading("status", text="สถานะ")

    table.column("id", width=50, anchor="center")
    table.column("name", width=220)
    table.column("category", width=120)
    table.column("size", width=70, anchor="center")
    table.column("price", width=100, anchor="e")
    table.column("status", width=120, anchor="center")
    table.pack(fill="both", expand=True, padx=20, pady=10)

    def load_data():
        for row in table.get_children():
            table.delete(row)
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT costumes.costume_id, costumes.costume_name, categories.category_name, 
                   costumes.size, costumes.rental_price, costumes.status
            FROM costumes
            JOIN categories ON costumes.category_id = categories.category_id
        """)
        for row in cursor.fetchall():
            table.insert("", "end", values=row)
        conn.close()

    def add_costume():
        c_name = e_name.get()
        c_cat = e_cat.get()
        c_size = e_size.get()
        c_price = e_price.get()
        
        if not c_name or not c_price:
            messagebox.showerror("แจ้งเตือน", "กรุณากรอกชื่อชุดและราคาให้ครบถ้วน")
            return
        
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO costumes (costume_name, category_id, size, rental_price, status) VALUES (?, ?, ?, ?, ?)",
                       (c_name, c_cat, c_size, float(c_price), "พร้อมใช้งาน"))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("สำเร็จ", "เพิ่มข้อมูลชุดใหม่เรียบร้อยแล้ว!")
        e_name.delete(0, tk.END)
        e_size.delete(0, tk.END)
        e_price.delete(0, tk.END)
        load_data()

    btn_add = tk.Button(form_frame, text="➕ บันทึกชุดใหม่", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), command=add_costume)
    btn_add.grid(row=0, column=4, rowspan=2, padx=15, ipadx=10, ipady=5)

    load_data()


# =========================
# หน้าต่างจัดการลูกค้า (เพิ่มลูกค้าได้จริง)
# =========================
def show_customers():
    window = tk.Toplevel(root)
    window.title("จัดการข้อมูลลูกค้า")
    window.geometry("800x480")

    title = tk.Label(window, text="👤 ระบบจัดการลูกค้า", font=("Arial", 18, "bold"))
    title.pack(pady=10)

    form_frame = tk.LabelFrame(window, text=" เพิ่มสมาชิกลูกค้าใหม่ ", font=("Arial", 11, "bold"), padx=10, pady=10)
    form_frame.pack(fill="x", padx=20, pady=5)

    tk.Label(form_frame, text="ชื่อ-นามสกุล:").grid(row=0, column=0, sticky="w", padx=5)
    e_cname = tk.Entry(form_frame, width=20)
    e_cname.grid(row=0, column=1, padx=5)

    tk.Label(form_frame, text="เบอร์โทรศัพท์:").grid(row=0, column=2, sticky="w", padx=5)
    e_phone = tk.Entry(form_frame, width=15)
    e_phone.grid(row=0, column=3, padx=5)

    tk.Label(form_frame, text="ที่อยู่:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    e_addr = tk.Entry(form_frame, width=35)
    e_addr.grid(row=1, column=1, columnspan=3, sticky="w", padx=5, pady=5)

    table = ttk.Treeview(window, columns=("id", "name", "phone", "address"), show="headings")
    table.heading("id", text="รหัสลูกค้า")
    table.heading("name", text="ชื่อ-นามสกุล")
    table.heading("phone", text="เบอร์โทรศัพท์")
    table.heading("address", text="ที่อยู่ / จังหวัด")
    table.column("id", width=80, anchor="center")
    table.column("name", width=200)
    table.column("phone", width=130, anchor="center")
    table.column("address", width=250)
    table.pack(fill="both", expand=True, padx=20, pady=10)

    def load_customers():
        for row in table.get_children():
            table.delete(row)
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT customer_id, customer_name, phone, address FROM customers")
        for row in cursor.fetchall():
            table.insert("", "end", values=row)
        conn.close()

    def add_customer():
        name = e_cname.get()
        phone = e_phone.get()
        addr = e_addr.get()
        
        if not name:
            messagebox.showerror("แจ้งเตือน", "กรุณากรอกชื่อลูกค้า")
            return
            
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO customers (customer_name, phone, address) VALUES (?, ?, ?)", (name, phone, addr))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("สำเร็จ", "เพิ่มลูกค้าใหม่เรียบร้อยแล้ว!")
        e_cname.delete(0, tk.END)
        e_phone.delete(0, tk.END)
        e_addr.delete(0, tk.END)
        load_customers()

    btn_add = tk.Button(form_frame, text="➕ เพิ่มลูกค้า", bg="#2196F3", fg="white", font=("Arial", 10, "bold"), command=add_customer)
    btn_add.grid(row=0, column=4, rowspan=2, padx=15, ipadx=10, ipady=5)

    load_customers()


# =========================
# หน้าต่างรายการเช่าชุด
# =========================
def show_rentals():
    window = tk.Toplevel(root)
    window.title("รายการเช่าชุด")
    window.geometry("850x450")

    title = tk.Label(window, text="🧾 ประวัติและรายการเช่าชุด", font=("Arial", 18, "bold"))
    title.pack(pady=15)

    table = ttk.Treeview(window, columns=("id", "customer", "costume", "r_date", "ret_date", "status"), show="headings")
    table.heading("id", text="รหัส")
    table.heading("customer", text="ชื่อลูกค้า")
    table.heading("costume", text="ชื่อชุดที่เช่า")
    table.heading("r_date", text="วันที่เช่า")
    table.heading("ret_date", text="กำหนดคืน")
    table.heading("status", text="สถานะ")

    table.column("id", width=50, anchor="center")
    table.column("customer", width=160)
    table.column("costume", width=180)
    table.column("r_date", width=100, anchor="center")
    table.column("ret_date", width=100, anchor="center")
    table.column("status", width=100, anchor="center")
    table.pack(fill="both", expand=True, padx=20, pady=10)

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT rentals.rental_id, customers.customer_name, costumes.costume_name, 
               rentals.rental_date, rentals.return_date, rentals.status
        FROM rentals
        JOIN customers ON rentals.customer_id = customers.customer_id
        JOIN costumes ON rentals.costume_id = costumes.costume_id
    """)
    for row in cursor.fetchall():
        table.insert("", "end", values=row)
    conn.close()


# =========================
# หน้าต่างคืนชุด
# =========================
def show_returns():
    window = tk.Toplevel(root)
    window.title("ระบบคืนชุด")
    window.geometry("500x350")

    title = tk.Label(window, text="🔄 ระบบทำรายการคืนชุด", font=("Arial", 18, "bold"))
    title.pack(pady=15)

    tk.Label(window, text="กรอกรหัสการเช่า (Rental ID):", font=("Arial", 11)).pack(pady=5)
    e_rid = tk.Entry(window, font=("Arial", 12), width=15, justify="center")
    e_rid.pack(pady=5)

    def process_return():
        rid = e_rid.get()
        if not rid:
            messagebox.showerror("แจ้งเตือน", "กรุณากรอกรหัสการเช่า")
            return
        messagebox.showinfo("สำเร็จ", f"ทำรายการคืนชุดสำหรับรหัสเช่าที่ {rid} เรียบร้อยแล้ว!")
        window.destroy()

    btn = tk.Button(window, text="✅ ยืนยันการคืนชุด", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", width=20, height=2, command=process_return)
    btn.pack(pady=20)


# =========================
# หน้าต่างรายงานสรุป
# =========================
def show_report():
    window = tk.Toplevel(root)
    window.title("รายงานสรุป")
    window.geometry("450x350")

    title = tk.Label(window, text="📊 รายงานสรุปภาพรวมร้าน", font=("Arial", 18, "bold"))
    title.pack(pady=15)

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM costumes")
    tc = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM customers")
    tcus = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM rentals")
    tr = cursor.fetchone()[0]
    conn.close()

    info = f"""
    ━━━━━━━━━━━━━━━━━━━━━━━━━
    👗 จำนวนชุดทั้งหมดในระบบ:   {tc} ชุด
    👥 จำนวนสมาชิกลูกค้า:       {tcus} คน
    🧾 รายการเช่าทั้งหมด:      {tr} รายการ
    ━━━━━━━━━━━━━━━━━━━━━━━━━
    """
    tk.Label(window, text=info, font=("Arial", 12), justify="left").pack(pady=10)


# =========================
# หน้าจอหลัก (Main Window)
# =========================
root = tk.Tk()
root.title("ระบบจัดการร้านเช่าชุด (Demo System)")
root.geometry("680x480")
root.resizable(False, False)

tk.Label(root, text="👗 ระบบจัดการร้านเช่าชุด", font=("Arial", 22, "bold")).pack(pady=20)
tk.Label(root, text="Costume Rental Management System - Full Demo", font=("Arial", 11), fg="gray").pack(pady=2)

menu_frame = tk.Frame(root)
menu_frame.pack(pady=20)

tk.Button(menu_frame, text="👗\nจัดการชุด", width=16, height=3, font=("Arial", 11, "bold"), command=show_costumes).grid(row=0, column=0, padx=12, pady=10)
tk.Button(menu_frame, text="👤\nลูกค้า", width=16, height=3, font=("Arial", 11, "bold"), command=show_customers).grid(row=0, column=1, padx=12, pady=10)
tk.Button(menu_frame, text="🧾\nเช่าชุด", width=16, height=3, font=("Arial", 11, "bold"), command=show_rentals).grid(row=1, column=0, padx=12, pady=10)
tk.Button(menu_frame, text="🔄\nคืนชุด", width=16, height=3, font=("Arial", 11, "bold"), command=show_returns).grid(row=1, column=1, padx=12, pady=10)

tk.Button(root, text="📊 ดูรายงานสรุปภาพรวม", width=36, height=2, font=("Arial", 11, "bold"), bg="#FF9800", fg="white", command=show_report).pack(pady=5)

root.mainloop()