import requests

def verify_request_result(status_code: int) -> bool:
    """
        Check whether an HTTP request was successful.

    Args:
        status_code (int): HTTP status code returned by the request.

    Returns:
        bool: True if the status code is 2xx, False otherwise.
    """
    if 200 <= status_code < 300:
        return True
    else:
        return False


def get_latitude_longitude(country_code: str, state_code: str, city_name: str) -> tuple[float, float]:
    """
    Retrieve latitude and longitude for a given city using a geocoding service.

    Args:
        country_code (str): ISO 3166-1 alpha-2 country code (e.g. "BR").
        state_code (str): State or region code (e.g. "SP").
        city_name (str): City name.

    Returns:
        tuple[float, float]: Latitude and longitude in decimal degrees (WGS84).

    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
        SystemExit: If the location cannot be resolved.
    """
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": f"{city_name} {state_code} {country_code}",
        "format": "json",
        "limit": 1
    }

    try:
        res = requests.get(url, headers={"User-Agent": "meu-app"}, params=params)

    except requests.exceptions.RequestException as e:
        raise LookupError(f"Unable to resolve location | {e}")

    if verify_request_result(res.status_code):
        data = res.json()
        return float(data[0]["lat"]), float(data[0]["lon"])
        
    else:
        raise requests.exceptions.RequestException(f"Error fetching data | Status code: {res.status_code}")
