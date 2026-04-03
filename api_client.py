import os
import requests
from dotenv import load_dotenv

load_dotenv()
SERPAPI_KEY = os.environ.get('SERPAPI_KEY')


def get_flight_details(origin: str, destination: str, outbound_date: str, return_date: str = None) -> dict | None:
    """
    Fetches real-time flight data from Google Flights via SerpApi.
    Supports both one-way and round-trip (if return_date is provided).
    """
    try:
        # Define API parameters for the Google Flights engine
        params = {
            "engine": "google_flights",
            "departure_id": origin,
            "arrival_id": destination,
            "outbound_date": outbound_date,
            "currency": "PLN",
            "hl": "en",  # Results in English for consistent AI analysis
            "api_key": SERPAPI_KEY
        }

        # Determine trip type based on presence of return date
        if return_date:
            params["type"] = "1"  # Round trip
            params["return_date"] = return_date
        else:
            params["type"] = "2"  # One way

        # Execute HTTP GET request
        response = requests.get("https://serpapi.com/search", params=params)
        data = response.json()

        # Error handling for API-side issues
        if "error" in data:
            print(f"  [DEBUG] SerpApi Error: {data['error']}")
            return None

        # Check if any flights were returned
        if "best_flights" not in data and "other_flights" not in data:
            return None

        # Priority: select 'best_flights' if available, otherwise 'other_flights'
        best_offer = data.get("best_flights", data.get("other_flights", []))[0]
        flights = best_offer.get("flights", [])

        # Extract and format trip duration
        duration_mins = best_offer.get("total_duration", 0)
        formatted_duration = f"{duration_mins // 60}h {duration_mins % 60}m"

        return {
            "price": float(best_offer.get("price")),
            "currency": "PLN",
            "duration": formatted_duration,
            "stops": len(flights) - 1,
            "carrier": flights[0].get("airline", "Unknown Carrier")
        }
    except Exception as error:
        print(f"  [DEBUG] Critical API Error: {error}")
        return None