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
        # FIXED: Added the full endpoint path and query parameter
        url = f"https://openexchangerates.org/api/latest.json?app_id={app_id}"

        
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        self.rates = data["rates"]
        # Ensure USD is present as the base
        self.rates["USD"] = 1.0 
        
        self.last_updated = time.time()
        self.available_currencies = sorted(self.rates.keys())

    def convert(self, amount, from_cur, to_cur) -> float:
        if from_cur == to_cur:
            return amount
        
        # FIXED: Cross-rate math for non-USD starting currencies
        if from_cur in self.rates and to_cur in self.rates:
            # Step 1: Divide by from_cur rate to get USD value
            # Step 2: Multiply by to_cur rate to get final value
            total = (amount / self.rates[from_cur]) * self.rates[to_cur]
        else:
            print(f"Error: {from_cur} or {to_cur} not found!")
            return 0.0
        
        note = f"{amount} {from_cur} is {total:.2f} {to_cur}"
        self.history.append(note)
        return total

    def get_history(self) -> list:
        return self.history
    
    def clear_history(self):
        self.history = []
