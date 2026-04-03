import os
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))


class FlightAnalysis(BaseModel):
    """Structured evaluation of a flight offer."""
    is_gem: bool = Field(description="Is this flight an exceptional price deal?")
    score: int = Field(description="Offer rating from 1 to 10")
    summary: str = Field(description="2-sentence summary of the offer quality")
    pros: List[str] = Field(description="Key advantages (e.g., direct, cheap)")
    cons: List[str] = Field(description="Key disadvantages (e.g., long layover)")


def analyze_with_ai(flight_data: dict, baseline: dict, trip_type_desc: str) -> FlightAnalysis:
    """
    Compares live flight data against AI-generated market baselines
    to provide a final verdict and score.
    """
    prompt = f"""
    Analyze the following flight route: {baseline['origin']} -> {baseline['dest']}.
    Trip type: {trip_type_desc}.
    Live price found: {flight_data['price']} PLN.
    Market average for {trip_type_desc}: {baseline['avg_price']} PLN. (Deal threshold: {baseline['threshold']} PLN).
    Flight info: {flight_data['stops']} stops, duration: {flight_data['duration']}.
    """

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": "You are a rigorous flight data analyst. Be honest and critical."},
            {"role": "user", "content": prompt}
        ],
        response_format=FlightAnalysis,
    )

    return completion.choices[0].message.parsed