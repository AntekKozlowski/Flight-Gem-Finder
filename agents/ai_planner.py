import os
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))


class Route(BaseModel):
    """Pydantic model representing a single flight route and its associated costs."""
    origin: str = Field(description="3-letter IATA code of the departure airport")
    dest: str = Field(description="3-letter IATA code of the arrival airport")
    avg_price: int = Field(description="Estimated market price in PLN for the chosen trip type")
    threshold: int = Field(description="Price in PLN below which the flight is considered a 'gem' deal")
    transfer_cost: int = Field(
        description="Estimated ground transport cost in PLN (train/bus) if airports differ from the exact query. Put 0 if no extra transfer is needed.")
    transfer_notes: str = Field(
        description="Brief note about ground transport (e.g., 'Bus Larnaca-Nicosia: ~30 PLN, 50 mins', 'Direct')")


class RouteList(BaseModel):
    """Container for the list of generated routes."""
    routes: List[Route] = Field(description="List of 3 to 5 optimal travel routes")


def generate_routes_for_query(user_query: str, trip_type_desc: str) -> List[dict]:
    """
    Acts as the Geography & Planning Agent.
    Translates a vague user query into a list of specific IATA route combinations,
    estimating hidden ground transport costs for alternative airports.
    """
    prompt = f"""
    User is looking for flights: "{user_query}".
    Trip type: {trip_type_desc}.

    Task: Generate up to 5 sensible IATA airport combinations.
    If you select alternative airports (e.g., LCA for Nicosia, or KRK for someone in Warsaw), 
    estimate the ground transportation cost (transfer_cost) to get there and provide brief transfer_notes.
    Also, estimate a baseline market flight price in PLN and a "gem threshold".
    """

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {
                "role": "system",
                "content": "You are an expert travel planner fluent in IATA codes, global flight pricing, and local ground transportation."
            },
            {"role": "user", "content": prompt}
        ],
        response_format=RouteList,
    )

    return [route.model_dump() for route in completion.choices[0].message.parsed.routes]