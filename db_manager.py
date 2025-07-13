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