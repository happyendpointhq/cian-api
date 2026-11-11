"""Minimal client for the Cian API on RapidAPI.

Set RAPIDAPI_KEY in your environment (or in a .env file at the repo root).
"""

import os
from datetime import datetime, timezone

import requests

HOST = "cian-ru.p.rapidapi.com"


def _load_dotenv():
    """Read RAPIDAPI_KEY from a .env in the current folder or the repo root, if present."""
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
    for path in (".env", os.path.join(root, ".env")):
        if os.path.exists(path):
            for line in open(path, encoding="utf-8"):
                key, sep, value = line.strip().partition("=")
                if sep and value and not key.startswith("#"):
                    os.environ.setdefault(key.strip(), value.strip())


_load_dotenv()


def get(path, **params):
    """GET an endpoint and return the `data` object of the response."""
    key = os.environ.get("RAPIDAPI_KEY")
    if not key:
        raise SystemExit("Set RAPIDAPI_KEY first (see .env.example).")
    response = requests.get(
        f"https://{HOST}{path}",
        params={k: v for k, v in params.items() if v is not None},
        headers={"x-rapidapi-host": HOST, "x-rapidapi-key": key},
        timeout=60,
    )
    response.raise_for_status()
    body = response.json()
    if not body.get("success", True):
        raise RuntimeError(f"{path} failed: {body}")
    return body["data"]


def to_date(value):
    """Cian timestamps come in two units: Unix seconds in price history, Unix
    milliseconds in valuation history. ISO strings (created_at) are passed through."""
    if value is None:
        return None
    if isinstance(value, str):
        return datetime.fromisoformat(value[:19]).date()
    seconds = value / 1000 if value > 10**11 else value
    return datetime.fromtimestamp(seconds, tz=timezone.utc).date()


def rub(value):
    return f"{value:,.0f} RUB".replace(",", " ") if value is not None else "-"
