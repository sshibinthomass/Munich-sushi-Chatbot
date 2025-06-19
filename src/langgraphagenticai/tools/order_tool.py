import json
from mcp.server.fastmcp import FastMCP
import os
mcp = FastMCP("OrderTool", port=8001)

@mcp.tool()
def place_order(restaurant: str, items: list, customer_name: str) -> dict:
    """
    Place an order at a restaurant.

    Args:
        restaurant (str): The name of the restaurant. eg. Sasou
        items (list): A list of items, each item is a dict with 'name' and 'quantity'. eg. [{"name": "Salmon Sushi", "quantity": 1}, {"name": "Miso Soup", "quantity": 2}]
        customer_name (str): The name of the customer. eg. John Doe

    Returns:
        dict: The order details, including order_id, restaurant, items, customer_name, and status.
    """
    try:
        orders_file = 'data/orders.json'
        if not os.path.exists(orders_file) or os.path.getsize(orders_file) == 0:
            orders = []
        else:
            with open(orders_file, 'r', encoding='utf-8') as f:
                orders = json.load(f)
        order_id = len(orders) + 1
        order = {
            "order_id": order_id,
            "restaurant": restaurant,
            "items": items,
            "customer_name": customer_name,
            "status": "pending"
        }
        orders.append(order)
        with open(orders_file, 'w', encoding='utf-8') as f:
            json.dump(orders, f, indent=2)
        return order
    except Exception as e:
        print(f"Error placing order: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run(transport="streamable-http")