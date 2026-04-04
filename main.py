import sys

sys.stdout.reconfigure(encoding='utf-8')

from core.database import setup_database, save_flight_record
from agents.ai_planner import generate_routes_for_query
from core.api_client import get_flight_details
from agents.agent import analyze_with_ai


def main():
    """
    Main application entry point.
    Handles user interaction, orchestrates AI agents, and manages the execution flow.
    """
    setup_database()

    print("=" * 50)
    print("🌍 AUTONOMOUS FLIGHT GEM FINDER AGENT 🌍")
    print("=" * 50)

    user_interest = input("Where do you want to go? (e.g., 'Poland - Nicosia'): ")
    trip_choice = input("One-way (1) or Round-trip (2)? Enter 1 or 2: ")
    target_date = input("Departure date (YYYY-MM-DD): ")

    return_date = None
    trip_type_desc = "one-way"

    if trip_choice == "2":
        return_date = input("Return date (YYYY-MM-DD): ")
        trip_type_desc = "round-trip"

    print(f"\n🧠 Agent Planner is mapping geography for a {trip_type_desc} trip...")
    dynamic_routes = generate_routes_for_query(user_interest, trip_type_desc)

    print(f"✅ Found {len(dynamic_routes)} optimal routes. Querying live data...\n")

    for route in dynamic_routes:
        print(f"✈️ Checking: {route['origin']} -> {route['dest']} (Market avg: {route['avg_price']} PLN)")

        flight = get_flight_details(route['origin'], route['dest'], target_date, return_date)

        if flight:
            analysis = analyze_with_ai(flight, route, trip_type_desc)

            save_flight_record(
                origin=route['origin'],
                dest=route['dest'],
                price=flight['price'],
                is_gem=analysis.is_gem,
                score=analysis.score
            )

            if analysis.is_gem:
                print(f"  💎 GEM FOUND! ({flight['price']} PLN)")
            else:
                print(f"  💰 Current Price: {flight['price']} PLN (No deal)")

            print(f"  ✈️  Airline: {flight['carrier']}")
            print(f"  🕒 Times: Departure {flight['departure_time']} | Arrival {flight['arrival_time']}")

            if route['transfer_cost'] > 0:
                print(f"  🚌 Ground Transport: {route['transfer_notes']} (Est. {route['transfer_cost']} PLN)")
                print(f"  💵 TOTAL ESTIMATED COST: {flight['price'] + route['transfer_cost']} PLN")

            if flight['stops'] > 0:
                print(f"  🔄 Layovers: {flight['layovers']} ({flight['duration']} total)")
            else:
                print(f"  ✅ Direct flight ({flight['duration']})")

            print(f"  ⭐ Score: {analysis.score}/10 | {analysis.summary}")

            if analysis.cons:
                print(f"  ⚠️ Watch out for: {', '.join(analysis.cons)}")
        else:
            print("  ❌ No live flights found for these specific dates/routes.")

        print("-" * 50)


if __name__ == "__main__":
    main()