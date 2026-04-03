import pytest
from unittest.mock import patch
from api_client import get_flight_details


# We use the @patch decorator to intercept the 'requests.get' call
# This prevents the test from making real network requests and spending API credits.
@patch('api_client.requests.get')
def test_get_flight_details_success(mock_get):
    """
    Test a successful flight data retrieval scenario.
    Checks if the data is correctly parsed and formatted by our function.
    """

    # 1. SETUP: Create a fake (mock) response that mimics SerpApi's structure
    mock_response = mock_get.return_value
    mock_response.json.return_value = {
        "best_flights": [{
            "price": 1500,
            "total_duration": 150,  # 150 minutes should be converted to 2h 30m
            "flights": [
                {"airline": "LOT Polish Airlines"}
            ]
        }]
    }

    # 2. EXECUTION: Call our real function with the mocked environment
    result = get_flight_details("WAW", "LHR", "2026-10-10")

    # 3. ASSERTION: Verify that the function logic works as expected
    assert result is not None, "The function should return a dictionary, not None"
    assert result["price"] == 1500.0
    assert result["currency"] == "PLN"

    # Check if our duration formatting logic (mins -> hours/mins) is correct
    assert result["duration"] == "2h 30m"

    assert result["stops"] == 0, "One flight segment should equal zero stops/layovers"
    assert result["carrier"] == "LOT Polish Airlines"


@patch('api_client.requests.get')
def test_get_flight_details_no_results(mock_get):
    """
    Test the scenario where the API returns no flight results.
    Ensures the application handles empty data gracefully.
    """

    # SETUP: Mock an empty response from SerpApi
    mock_response = mock_get.return_value
    mock_response.json.return_value = {
        "search_metadata": {"status": "Success"},
        "error": "No flights found"  # Common API behavior when no results match
    }

    # EXECUTION
    result = get_flight_details("XYZ", "ABC", "2026-12-12")

    # ASSERTION: The function should return None when no flights are found
    assert result is None