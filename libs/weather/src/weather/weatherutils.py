import requests

def verify_request_result(status_code: int = None):
    if status_code == 200:
        return True
    else:
        return False


def get_latitude_longitude(country_code: str=None, state_code: str=None, city_name: str = None) -> tuple[float, float]:
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": f"{city_name} {state_code} {country_code}",
        "format": "json",
        "limit": 1
    }

    try:
        res = requests.get(url, headers={"User-Agent": "meu-app"}, params=params)

    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    if verify_request_result(res.status_code):
        data = res.json()
        return float(data[0]["lat"]), float(data[0]["lon"])
        
    else:
        raise requests.exceptions.RequestException(f"Error fetching data | Status code: {res.status_code}")
