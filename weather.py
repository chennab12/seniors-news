"""Today's Hyderabad weather and air quality from Open-Meteo (free, no API key)."""
import json
import urllib.request

from extras_content import HYDERABAD

FORECAST = (
    "https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&timezone=Asia%2FKolkata"
    "&current=temperature_2m,apparent_temperature,precipitation"
    "&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max&forecast_days=1"
)
AIR = "https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&timezone=Asia%2FKolkata&current=us_aqi"


def _get(url, timeout):
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (seniors-news app)"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.load(response)


def parse(forecast, air):
    current, daily = forecast["current"], forecast["daily"]
    return {
        "temp": current["temperature_2m"],
        "feels_like": current["apparent_temperature"],
        "max": daily["temperature_2m_max"][0],
        "min": daily["temperature_2m_min"][0],
        "rain_chance": daily["precipitation_probability_max"][0] or 0,
        "aqi": (air or {}).get("current", {}).get("us_aqi"),
    }


def fetch_weather(timeout=8):
    lat, lon = HYDERABAD
    forecast = _get(FORECAST.format(lat=lat, lon=lon), timeout)
    try:
        air = _get(AIR.format(lat=lat, lon=lon), timeout)
    except Exception:
        air = None  # weather is still useful without air quality
    return parse(forecast, air)
