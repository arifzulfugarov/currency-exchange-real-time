import requests
import time

class CurrencyConverter:
    def __init__(self):
        self.rates = {}
        self.last_updated = None
        self.available_currencies = []

    def fetch_rates(self, app_id: str):
        url = f"https://openexchangerates.org/api/latest.json?app_id={app_id}"

        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        self.rates = data["rates"]
        self.rates["USD"] = 1.0
        self.last_updated = time.time()
        self.available_currencies = sorted(self.rates.keys())

    def convert(self, amount, from_cur, to_cur, save_to_history=False) -> float:
        if from_cur == to_cur:
            return amount

        if from_cur in self.rates and to_cur in self.rates:
            return (amount / self.rates[from_cur]) * self.rates[to_cur]

        raise ValueError(f"{from_cur} or {to_cur} not found!")