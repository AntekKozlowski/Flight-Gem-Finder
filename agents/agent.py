import os
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))


class FlightAnalysis(BaseModel):
    """Pydantic model representing the AI's final verdict on a flight deal."""
    is_gem: bool = Field(description="Is this flight an exceptional price deal?")
    score: int = Field(description="Offer rating from 1 to 10 based on total cost and convenience")
    summary: str = Field(description="2-sentence summary of the offer quality")
    pros: List[str] = Field(description="Key advantages (e.g., direct flight, cheap base price)")
    cons: List[str] = Field(description="Key disadvantages (e.g., long layover, expensive bus transfer)")


def analyze_with_ai(flight_data: dict, baseline: dict, trip_type_desc: str) -> FlightAnalysis:
    """
    Acts as the Data Analyst Agent.
    Evaluates live flight data against the baseline market prices, factoring in
    layovers, airlines, and hidden ground transport costs.
    """
    total_cost = flight_data['price'] + baseline['transfer_cost']

    prompt = f"""
    Analyze the following flight route: {baseline['origin']} -> {baseline['dest']}.
    Trip type: {trip_type_desc}.
    Live flight price found: {flight_data['price']} PLN.

    Ground Transport Info: {baseline['transfer_notes']} (Cost: {baseline['transfer_cost']} PLN)
    TOTAL TRIP COST (Flight + Transport): {total_cost} PLN.

    Market average for flight: {baseline['avg_price']} PLN. (Deal threshold: {baseline['threshold']} PLN).

    Detailed Flight Info:
    - Airline(s): {flight_data['carrier']}
    - Departure: {flight_data['departure_time']}
    - Arrival: {flight_data['arrival_time']}
    - Total Duration: {flight_data['duration']}
    - Stops: {flight_data['stops']} (Layover airports: {flight_data['layovers']})

    Critique this deal aggressively. Base your score on the TOTAL TRIP COST. 
    If the layover is terrible or the ground transport is too long/expensive, deduct points.
    """

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {
                "role": "system",
                "content": "You are a rigorous flight data analyst. Be honest and critical about hidden costs and travel fatigue."
            },
            {"role": "user", "content": prompt}
        ],
        response_format=FlightAnalysis,
    )

    return completion.choices[0].message.parsed