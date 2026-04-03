import sys

# Set console output to UTF-8 for cross-platform compatibility
sys.stdout.reconfigure(encoding='utf-8')

from ai_planner import generate_routes_for_query
from api_client import get_flight_details
from agent import analyze_with_ai


def main():
    """Main application loop and user interaction handler."""
    print("=" * 50)
    print("🌍 AUTONOMOUS FLIGHT GEM FINDER AGENT 🌍")
    print("=" * 50)

    # 1. Collect user requirements
    user_interest = input("Where do you want to go? (e.g., 'Poland - Japan'): ")
    trip_choice = input("One-way (1) or Round-trip (2)? Enter 1 or 2: ")
    target_date = input("Departure date (YYYY-MM-DD): ")

    return_date = None
    trip_type_desc = "one-way"

    if trip_choice == "2":
        return_date = input("Return date (YYYY-MM-DD): ")
        trip_type_desc = "round-trip"

    # 2. Agent 1: Planning and Market Baseline Estimation
    print(f"\n🧠 Agent Planner is mapping geography for a {trip_type_desc} trip...")
    dynamic_routes = generate_routes_for_query(user_interest, trip_type_desc)

    print(f"✅ Found {len(dynamic_routes)} optimal routes. Querying live data...\n")

    # 3. Execution: Iterate through suggested routes and fetch live data
    for route in dynamic_routes:
        print(f"✈️ Checking: {route['origin']} -> {route['dest']} (Market avg: {route['avg_price']} PLN)")

        flight = get_flight_details(route['origin'], route['dest'], target_date, return_date)

        if flight:
            # 4. Agent 2: Analysis and Scoring
            analysis = analyze_with_ai(flight, route, trip_type_desc)

            # Print Final Report
            if analysis.is_gem:
                print(f"  💎 GEM FOUND! ({flight['price']} PLN)")
            else:
                print(f"  💰 Current Price: {flight['price']} PLN (No deal)")

            print(f"  Score: {analysis.score}/10 | {analysis.summary}")
            if analysis.cons:
                print(f"  Watch out for: {', '.join(analysis.cons)}")
        else:
            print("  ❌ No live flights found for these specific dates/routes.")

        print("-" * 50)


if __name__ == "__main__":
    main()