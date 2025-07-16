import datetime
from db_manager import first_setup, add_customer, add_order, add_printjob, recalculate_order_cost, get_orders_for_customer, get_printjobs_for_order, get_customers
from gcode_parser import parse_gcode

def main():
    first_setup()
    print("Database ready.")

    # Add a test customer
    customer_name = "Jackie"
    add_customer(customer_name)
    print(f"Added customer: {customer_name}")

    # Get customer id (assume last inserted)
    customers = get_customers()
    customer_id = customers[-1][0]  # last customer

    # Create a new order for today
    order_date = datetime.date.today().isoformat()
    add_order(customer_id, order_date)
    print(f"Order created for customer ID {customer_id} on {order_date}")

    # Get the order id (last inserted)
    orders = get_orders_for_customer(customer_id)
    order_id = orders[-1][0]

    # Parse G-code file (put your path here)
    filepath = "example.gcode"
    filament_g, print_time = parse_gcode(filepath)
    print(f"Parsed G-code: {filament_g}g filament, {print_time} min print time")

    # Add print job
    add_printjob(order_id, filepath, filament_g, print_time)
    print("Print job added.")

    # Recalculate cost (use your filament cost per kg, e.g. 25.0)
    filament_cost_per_kg = 25.0
    recalculate_order_cost(order_id, filament_cost_per_kg)
    print("Order cost recalculated.")

    # Print order summary
    orders = get_orders_for_customer(customer_id)
    printjobs = get_printjobs_for_order(order_id)

    print("\n--- Order Summary ---")
    print(f"Customer: {customer_name}")
    print(f"Order ID: {order_id}, Date: {order_date}")
    print(f"Print Jobs:")
    for job in printjobs:
        print(f"  Item: {job[0]}, Filament: {job[1]}g, Time: {job[2]} min")
    print(f"Total orders for {customer_name}: {len(orders)}")

if __name__ == "__main__":
    main()
