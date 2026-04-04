from unittest.mock import patch
from core.api_client import get_flight_details

@patch('api_client.requests.get')
@patch('api_client.get_cached_flight')
def test_get_flight_details_success(mock_get_cached, mock_get):
    """Tests successful flight data retrieval and parsing, bypassing the cache."""
    mock_get_cached.return_value = None

    mock_response = mock_get.return_value
    mock_response.json.return_value = {
        "best_flights": [{
            "price": 1500,
            "total_duration": 150,
            "flights": [
                {
                    "airline": "LOT Polish Airlines",
                    "departure_airport": {"id": "WAW", "time": "2026-10-10 10:00"},
                    "arrival_airport": {"id": "LHR", "time": "2026-10-10 11:30"}
                }
            ]
        }]
    }

    with patch('api_client.save_cached_flight'):
        result = get_flight_details("WAW", "LHR", "2026-10-10")

    assert result is not None
    assert result["price"] == 1500.0
    assert result["duration"] == "2h 30m"
    assert result["stops"] == 0
    assert result["carrier"] == "LOT Polish Airlines"
    assert result["departure_time"] == "2026-10-10 10:00"
    assert result["layovers"] == "Direct"

@patch('api_client.requests.get')
@patch('api_client.get_cached_flight')
def test_get_flight_details_no_results(mock_get_cached, mock_get):
    """Tests the module's behavior when the API returns no viable flights."""
    mock_get_cached.return_value = None
    mock_response = mock_get.return_value
    mock_response.json.return_value = {
        "search_metadata": {"status": "Success"},
        "error": "No flights found"
    }

    result = get_flight_details("XYZ", "ABC", "2026-12-12")
    assert result is None