import requests
import time


class CurrencyConverter:
    def __init__(self):
        self.rates = {}
        self.history = []
        self.last_updated = None
        self.available_currencies = []

    def fetch_rates(self, app_id: str):
        self.app_id = app_id
        # Correct endpoint for the latest rates
        url = f"https://openexchangerates.org{self.app_id}"
        
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        self.rates = data["rates"]
        # We must also add 'USD' to the rates as 1.0 because it's the base
        self.rates["USD"] = 1.0 
        
        self.last_updated = time.time()
        self.available_currencies = sorted(self.rates.keys())


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




