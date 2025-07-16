import sqlite3

# Creates tables 
def first_setup():
    con = sqlite3.connect("database.db")
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS Customer (
            customer_id INTEGER PRIMARY KEY,
            customer_name VARCHAR(50) NOT NULL
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS T_Order (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            order_date DATE NOT NULL,
            delivery_cost DECIMAL(4,2),
            other_jobs_cost DECIMAL(4,2),
            markup_percentage DECIMAL(4,2),
            maintenance_cost DECIMAL(3,2),
            total_cost DECIMAL (6,2),
            FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
        );
        """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS PrintJob (
            job_id INTEGER PRIMARY KEY,
            order_id INTEGER NOT NULL,
            item_name VARCHAR(50) NOT NULL,
            filament_used_g INTEGER,
            print_time_min INTEGER,
            FOREIGN KEY (order_id) REFERENCES T_Order(order_id)
        );
        """)
    
    con.commit()
    con.close()
    
# Deletes the entire DB
def destroyer():
    con = sqlite3.connect("database.db")
    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS Customer ")
    cur.execute("DROP TABLE IF EXISTS T_Order")
    cur.execute("DROP TABLE IF EXISTS PrintJob")
    
    con.commit()
    con.close()

def add_customer(name):
    con = sqlite3.connect("database.db")
    cur = con.cursor()

    cur.execute("INSERT INTO Customer (customer_name) VALUES (?)", (name,))
    
    con.commit()
    con.close()

# maintenance cost should be calculated from summed print times
# total cost should be calculated from all the printjobs
def add_order(customer_id, 
              order_date, 
              delivery_cost=0.0, 
              other_jobs_cost=0.0, 
              markup_pct=20.0, 
              maintenance_cost_pct=20.0):

    con = sqlite3.connect("database.db")
    cur = con.cursor()

    cur.execute("""
        INSERT INTO T_Order 
        (customer_id, order_date, delivery_cost, other_jobs_cost, markup_percentage, maintenance_cost)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (customer_id, order_date, delivery_cost, other_jobs_cost, markup_pct, maintenance_cost_pct))

    con.commit()
    con.close()

def add_printjob(order_id, item_name, filament_used_g, print_time_min):
    con = sqlite3.connect("database.db")
    cur = con.cursor()

    cur.execute("""
        INSERT INTO PrintJob
        (order_id, item_name, filament_used_g, print_time_min)
        VALUES (?, ?, ?, ?)
    """, (order_id, item_name, filament_used_g, print_time_min))

    con.commit()
    con.close()

def get_customers():
    con = sqlite3.connect("database.db")
    cur = con.cursor()

    cur.execute("SELECT customer_id, customer_name FROM Customer")
    rows = cur.fetchall()

    con.close()
    return rows  # list of (id, name)

def get_orders_for_customer(customer_id):
    con = sqlite3.connect("database.db")
    cur = con.cursor()

    cur.execute("""
        SELECT order_id, order_date, total_cost
        FROM T_Order
        WHERE customer_id = ?
    """, (customer_id,))

    rows = cur.fetchall()
    con.close()
    return rows

def get_printjobs_for_order(order_id):
    con = sqlite3.connect("database.db")
    cur = con.cursor()

    cur.execute("""
        SELECT item_name, filament_used_g, print_time_min
        FROM PrintJob
        WHERE order_id = ?
    """, (order_id,))

    rows = cur.fetchall()
    con.close()
    return rows

def recalculate_order_cost(order_id, filament_cost_per_kg):
    con = sqlite3.connect("database.db")
    cur = con.cursor()

    # Get all printjobs for this order
    cur.execute("""
        SELECT filament_used_g, print_time_min
        FROM PrintJob
        WHERE order_id = ?
    """, (order_id,))
    jobs = cur.fetchall()

    total_filament_g = sum(row[0] or 0 for row in jobs)
    total_time_min = sum(row[1] or 0 for row in jobs)

    filament_cost = (total_filament_g / 1000) * filament_cost_per_kg
    maintenance_cost = total_time_min * 0.01  # ← tweak this rate later

    # Get base order costs
    cur.execute("""
        SELECT delivery_cost, other_jobs_cost, markup_percentage
        FROM T_Order
        WHERE order_id = ?
    """, (order_id,))
    delivery_cost, other_jobs_cost, markup_pct = cur.fetchone()

    subtotal = filament_cost + delivery_cost + other_jobs_cost + maintenance_cost
    markup = subtotal * (markup_pct / 100)
    total = subtotal + markup

    # Update the order
    cur.execute("""
        UPDATE T_Order
        SET maintenance_cost = ?,
            total_cost = ?
        WHERE order_id = ?
    """, (maintenance_cost, total, order_id))

    con.commit()
    con.close()


# __TABLES__
"""
CREATE TABLE IF NOT EXISTS Customer (
    customer_id INTEGER PRIMARY KEY,
    customer_name VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS T_Order (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date DATE NOT NULL,
    delivery_cost DECIMAL(4,2),
    other_jobs_cost DECIMAL(4,2),
    markup_percentage DECIMAL(4,2),
    maintenance_cost_percentage DECIMAL(3,2),
    total_cost DECIMAL (6,2),
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
);

CREATE TABLE IF NOT EXISTS PrintJob (
    job_id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    item_name VARCHAR(50) NOT NULL,
    filament_used_g INTEGER,
    print_time_min INTEGER,
    FOREIGN KEY (order_id) REFERENCES T_Order(order_id)
);
"""