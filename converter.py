import requests
import time


class CurrencyConverter:
    def __init__(self):
        self.rates = {}
        self.history = []
        self.last_updated = None
        self.available_currencies = []

    def fetch_rates(self, base_currency: str):

        url = f"https://api.frankfurter.app/latest?from={base_currency}"
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        if "rates" not in data:
            raise ValueError('Invalid API response')
        self.rates = data["rates"]
        self.base_currency = data["base"]
        self.last_updated = time.time()
        self.available_currencies = list(self.rates.keys())
        self.available_currencies.append(base_currency)
        self.available_currencies.sort()

    def convert(self, amount, from_cur, to_cur) -> float:

        if from_cur == to_cur:
            return amount
        
        if to_cur in self.rates:
            rate = self.rates[to_cur]
            total = amount * rate
        else:
            print(f"Error: {to_cur} not found!")
            return 0.0
        
        note = f"{amount} {from_cur} in {to_cur} is {total:.2f}"
        self.history.append(note)
        return total

    def get_history(self) -> list:
        
        return self.history
    
    def clear_history(self):

        self.history = []




