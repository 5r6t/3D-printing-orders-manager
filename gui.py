import tkinter as tk
from tkinter import ttk
import db_manager as dbm
from datetime import datetime

# Function for submit buttons, use like:
## submit_button = tk.Button(..., command=lambda: update_status(status_label, f"text"))
def update_status(status_label, info_text):
    info = info_text.strip
    if info:
        status_label.config(text=info)
    else:
        status_label.config(text="Programmer forgot, dunno what happened.")

def refresh_orders_df(display_frame):
    all_orders = []

    customers = dbm.get_customers()
    for cid, name in customers:
        orders = dbm.get_orders_for_customer(cid)
        for order_id, date_str, total_cost in orders:
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                continue
            if total_cost is None:
                total_cost = 0.0
            all_orders.append((name, order_id, date_obj.date(), f"€{total_cost:.2f}"))

    all_orders.sort()
    display_frame.update_data(all_orders)


#------------------------------------
import tkinter as tk
from tkinter import ttk

class DisplayFrame(ttk.Frame):
    def __init__(self, parent, columns, heading_text, **kwargs):
        super().__init__(parent, **kwargs)
        
        tk.Label(self, text=heading_text, bg="#2C2C2C", fg="white", font=('Arial', 12, 'bold')).pack(anchor="w", pady=(0,5))
        
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Treeview",
                        background="#2C2C2C",
                        foreground="white",
                        fieldbackground="#2C2C2C",
                        font="Arial",
                        borderwidth=0,
                        relief="solid")
        style.map("Treeview",
                  background=[('selected', '#88304E')],
                  foreground=[('selected', 'white')],
                  font="Arial")
        style.configure("Treeview.Heading",
                        foreground="white")
        style.map("Treeview.Heading",
                  background=[('active', '#F7374F')])

        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=15)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="w", width=100)

        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

    def update_data(self, data):
        self.tree.delete(*self.tree.get_children())
        for row in data:
            self.tree.insert("", tk.END, values=row)

#------------------------------------

root = tk.Tk()
root.title("3D Printing Order Manager")
root.configure(background="#000")
# ----- Main frames -----
frame_tl = tk.Frame(root, bg='red')
frame_tr = tk.Frame(root, bg='cyan')
frame_bl = tk.Frame(root, bg='green')
frame_br = tk.Frame(root, bg='yellow')

frame_tl.grid(row=0, column=0, sticky='nsew')
frame_tr.grid(row=0, column=1, sticky='nsew')
frame_bl.grid(row=1, column=0, sticky='nsew')
frame_br.grid(row=1, column=1, sticky='nsew')

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# ----- Menu -----
menu = tk.Menu(root)
file_menu_n = tk.Menu(menu, tearoff=0)
file_menu_n.add_command(label='New customer')
file_menu_n.add_command(label='New order')

file_menu_r = tk.Menu(menu, tearoff=0)
file_menu_r.add_command(label='Remove customer') # keep or remove his orders option too
file_menu_r.add_command(label='Remove order')

file_menu_e = tk.Menu(menu, tearoff=0)
file_menu_e.add_command(label='Edit customer')
file_menu_e.add_command(label='Edit order')

menu.add_cascade(label='New', menu=file_menu_n)
menu.add_cascade(label='Remove', menu=file_menu_r)
menu.add_cascade(label='Edit', menu=file_menu_e)
root.config(menu=menu)

# --- Content of individual main frames ---
orders_frame = DisplayFrame(frame_br, ["Customer", "Order ID", "Date", "Cost"], "Orders")
orders_frame.pack(fill="both", expand=True)

customers_frame = DisplayFrame(frame_tl, ["Customer", "Order ID", "Date", "Cost"], "Customers")
customers_frame.pack(fill="both", expand=True)
# ----- Final steps -----

refresh_orders_df(orders_frame)
root.mainloop()


# __Color_Theme__
"""
F7374F red
88304E maroon
522546 purple
2C2C2C black
"""