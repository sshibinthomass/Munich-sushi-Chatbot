import json
import sys
import requests
from pathlib import Path
from typing import List, Dict
from mcp.server.fastmcp import FastMCP
import time
from functools import wraps

current_file = Path(__file__).resolve()
project_root = current_file.parent.parent.parent.parent
sys.path.append(str(project_root))


mcp=FastMCP("Parking near restaurant", port=8003)

@mcp.tool()
def get_parking_data() -> dict:
    """
    Get available parking spaces in Munich.
    Returns:
        dict: The details about the available parking spaces in Munich.
    """
    with open(project_root / "data/parking.json", "r", encoding="utf-8") as f:
        return json.load(f)

@mcp.tool()
def get_open_parking_lots() -> List[Dict]:
    """
    Get all parking lots that are currently open.
    Returns:
        List[Dict]: Currently open parking lots with details
    """
    try:
        with open(project_root / "data/parking.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        
        open_lots = []
        for lot in data:
            business_hours = lot.get("businessHours", {})
            if business_hours.get("currentStatus") == "OPEN":
                open_lots.append({
                    "title": lot.get("title"),
                    "address": lot.get("address"),
                    "distance": lot.get("distance_from_current_location"),
                    "duration": lot.get("duration_from_current_location"),
                    "price_summary": lot.get("priceSummary", {}).get("priceSummaryText"),
                    "free_spots": lot.get("parking", {}).get("freeSpotsNumber"),
                    "total_spots": lot.get("parking", {}).get("spotsNumber"),
                    "next_status_change": business_hours.get("nextStatusChange")
                })
        
        return open_lots
    except Exception as e:
        return [{"error": str(e)}]

@mcp.tool()
def get_parking_with_free_spots() -> List[Dict]:
    """
    Get parking lots that currently have free spots available.
    Returns:
        List[Dict]: Parking lots with available spots
    """
    try:
        with open(project_root / "data/parking.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        
        available_lots = []
        for lot in data:
            parking_info = lot.get("parking", {})
            free_spots = parking_info.get("freeSpotsNumber")
            
            if free_spots and free_spots > 0:
                available_lots.append({
                    "title": lot.get("title"),
                    "address": lot.get("address"),
                    "free_spots": free_spots,
                    "total_spots": parking_info.get("spotsNumber"),
                    "availability_percentage": round((free_spots / parking_info.get("spotsNumber", 1)) * 100, 1),
                    "distance": lot.get("distance_from_current_location"),
                    "price_summary": lot.get("priceSummary", {}).get("priceSummaryText")
                })
        
        return sorted(available_lots, key=lambda x: x["free_spots"], reverse=True)
    except Exception as e:
        return [{"error": str(e)}]
    
@mcp.tool()
def get_parking_near_restaurant(restaurant_name: str) -> List[Dict]:
    """
    Get parking lots near a specific restaurant.
    Args:
        restaurant_name (str): The name of the restaurant
    Returns:
        List[Dict]: Parking lots near the restaurant
    """
    try:
        # First get restaurant location
        with open(project_root / "data/sushi.json", "r", encoding="utf-8") as f:
            restaurant_data = json.load(f)
        
        restaurant_location = None
        for restaurant in restaurant_data:
            if restaurant.get("title") == restaurant_name:
                restaurant_location = restaurant.get("position")
                break
        
        if not restaurant_location:
            return [{"error": f"Restaurant '{restaurant_name}' not found"}]
        
        # Get parking lots
        with open(project_root / "data/parking.json", "r", encoding="utf-8") as f:
            parking_data = json.load(f)
        
        nearby_lots = []
        for lot in parking_data:
            lot_position = lot.get("position", {})
            distance = lot.get("distance_from_current_location", "")
            
            nearby_lots.append({
                "title": lot.get("title"),
                "address": lot.get("address"),
                "distance": distance,
                "duration": lot.get("duration_from_current_location"),
                "price_summary": lot.get("priceSummary", {}).get("priceSummaryText"),
                "free_spots": lot.get("parking", {}).get("freeSpotsNumber"),
                "current_status": lot.get("businessHours", {}).get("currentStatus")
            })
        
        return nearby_lots
    except Exception as e:
        return [{"error": str(e)}]

@mcp.tool()
def get_24_hour_parking() -> List[Dict]:
    """
    Get parking lots that are open 24 hours.
    Returns:
        List[Dict]: 24-hour parking lots
    """
    try:
        with open(project_root / "data/parking.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        
        all_day_lots = []
        for lot in data:
            business_hours = lot.get("businessHours", {})
            formatted_hours = business_hours.get("formattedHours", [])
            
            if any("24 hours" in hour for hour in formatted_hours):
                all_day_lots.append({
                    "title": lot.get("title"),
                    "address": lot.get("address"),
                    "distance": lot.get("distance_from_current_location"),
                    "price_summary": lot.get("priceSummary", {}).get("priceSummaryText"),
                    "free_spots": lot.get("parking", {}).get("freeSpotsNumber"),
                    "payment_methods": lot.get("paymentMethods", [])
                })
        
        return all_day_lots
    except Exception as e:
        return [{"error": str(e)}]
    
@mcp.tool()
def get_parking_with_disabled_access() -> List[Dict]:
    """
    Get parking lots with disabled parking spots.
    Returns:
        List[Dict]: Parking lots with disabled access
    """
    try:
        with open(project_root / "data/parking.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        
        disabled_lots = []
        for lot in data:
            parking_info = lot.get("parking", {})
            services = parking_info.get("services", [])
            
            if "DISABLED" in services:
                disabled_lots.append({
                    "title": lot.get("title"),
                    "address": lot.get("address"),
                    "disabled_spots": parking_info.get("disabledSpotsNumber"),
                    "total_spots": parking_info.get("spotsNumber"),
                    "distance": lot.get("distance_from_current_location"),
                    "price_summary": lot.get("priceSummary", {}).get("priceSummaryText")
                })
        
        return disabled_lots
    except Exception as e:
        return [{"error": str(e)}]

@mcp.tool()
def get_parking_payment_methods() -> Dict:
    """
    Get all available payment methods across parking lots.
    Returns:
        Dict: Payment methods and which lots accept them
    """
    try:
        with open(project_root / "data/parking.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        
        payment_methods = {}
        for lot in data:
            methods = lot.get("paymentMethods", [])
            for method in methods:
                if method not in payment_methods:
                    payment_methods[method] = []
                payment_methods[method].append({
                    "title": lot.get("title"),
                    "address": lot.get("address"),
                    "distance": lot.get("distance_from_current_location")
                })
        
        return payment_methods
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def calculate_parking_cost(lot_name: str, hours: float) -> Dict:
    """
    Calculate parking cost for a specific duration.
    Args:
        lot_name (str): The name of the parking lot
        hours (float): Number of hours to park
    Returns:
        Dict: Calculated parking cost
    """
    try:
        with open(project_root / "data/parking.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        
        for lot in data:
            if lot.get("title") == lot_name:
                price_list = lot.get("priceStructured", {}).get("listPrices", [])
                
                # Find the best rate for the given hours
                best_rate = None
                for price_item in price_list:
                    price_text = price_item.get("price", "")
                    if "24 hours" in price_text:
                        daily_rate = float(price_text.split("€")[0].strip())
                        if hours >= 24:
                            days = int(hours // 24)
                            remaining_hours = hours % 24
                            cost = (days * daily_rate) + (remaining_hours * daily_rate / 24)
                            best_rate = {"cost": round(cost, 2), "rate_type": "daily"}
                            break
                    elif "1 hour" in price_text:
                        hourly_rate = float(price_text.split("€")[0].strip())
                        cost = hours * hourly_rate
                        best_rate = {"cost": round(cost, 2), "rate_type": "hourly"}
                
                if best_rate:
                    return {
                        "parking_lot": lot_name,
                        "hours": hours,
                        "estimated_cost": best_rate["cost"],
                        "rate_type": best_rate["rate_type"],
                        "address": lot.get("address")
                    }
                else:
                    return {"error": f"Could not calculate cost for {lot_name}"}
        
        return {"error": f"Parking lot '{lot_name}' not found"}
    except Exception as e:
        return {"error": str(e)}

if __name__=="__main__":
    mcp.run(transport="streamable-http")
