import os
import requests
from dotenv import load_dotenv
from core.database import get_cached_flight, save_cached_flight

load_dotenv()
SERPAPI_KEY = os.environ.get('SERPAPI_KEY')


def get_flight_details(origin: str, destination: str, outbound_date: str, return_date: str = None) -> dict | None:
    """
    Fetches real-time flight data via SerpApi, prioritizing local SQLite cache to save API credits.
    Returns a dictionary with parsed flight metrics or None if no flights are found.
    """
    cached_data = get_cached_flight(origin, destination, outbound_date, return_date)
    if cached_data:
        print(f"  [CACHE] Found fresh data for {origin} -> {destination}. Skipping API call!")
        return cached_data

    try:
        params = {
            "engine": "google_flights",
            "departure_id": origin,
            "arrival_id": destination,
            "outbound_date": outbound_date,
            "currency": "PLN",
            "hl": "en",
            "api_key": SERPAPI_KEY,
            "type": "1" if return_date else "2"
        }

        if return_date:
            params["return_date"] = return_date

        response = requests.get("https://serpapi.com/search", params=params)
        data = response.json()

        if "error" in data:
            print(f"  [DEBUG] SerpApi Error: {data['error']}")
            return None

        if "best_flights" not in data and "other_flights" not in data:
            return None

        best_offer = data.get("best_flights", data.get("other_flights", []))[0]
        flights = best_offer.get("flights", [])

        duration_mins = best_offer.get("total_duration", 0)
        formatted_duration = f"{duration_mins // 60}h {duration_mins % 60}m"

        try:
            dep_time = flights[0]["departure_airport"]["time"]
            arr_time = flights[-1]["arrival_airport"]["time"]
        except KeyError:
            dep_time = "Unknown"
            arr_time = "Unknown"

        layovers = [flights[i]["arrival_airport"]["id"] for i in range(len(flights) - 1)] if len(flights) > 1 else []
        layovers_str = ", ".join(layovers) if layovers else "Direct"

        airlines = list(dict.fromkeys([f.get("airline", "Unknown") for f in flights]))
        carrier_str = " + ".join(airlines)

        flight_result = {
            "price": float(best_offer.get("price")),
            "currency": "PLN",
            "duration": formatted_duration,
            "stops": len(flights) - 1,
            "carrier": carrier_str,
            "departure_time": dep_time,
            "arrival_time": arr_time,
            "layovers": layovers_str
        }

        save_cached_flight(origin, destination, outbound_date, return_date, flight_result)
        return flight_result

    except Exception as error:
        print(f"  [DEBUG] Critical API Error: {error}")
        return None