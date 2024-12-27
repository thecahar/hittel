from typing import Any, Dict, Tuple, Callable

EXCHANGE_RATES: Dict[Tuple[str, str], float] = {
    ("USD", "CHF"): 0.91,
    ("CHF", "USD"): 1.1,
    ("EUR", "CHF"): 1.05,
    ("CHF", "EUR"): 0.95,
    ("USD", "EUR"): 0.85,
    ("EUR", "USD"): 1.18,
}

class Price:
    def __init__(self, value: int, currency: str) -> None:
        self.value: int = value
        self.currency: str = currency

    def __str__(self) -> str:
        return f"Price: {self.value} {self.currency}"

    def convert(self, to: str) -> "Price":
        if self.currency == to:
            return self

        rate = EXCHANGE_RATES.get((self.currency, to))
        if rate is None:
            raise ValueError(f"Conversion rate from {self.currency} to {to} not available.")

        return Price(value=int(self.value * rate), currency=to)

    def __add__(self, other: Any) -> "Price":
        if not isinstance(other, Price):
            raise ValueError("Can perform operation only with Price objects.")

        if self.currency != other.currency:
            middle_currency = "CHF"
            self_converted = self.convert(to=middle_currency)
            other_converted = other.convert(to=middle_currency)
            result = Price(
                value=self_converted.value + other_converted.value, currency=middle_currency
            ).convert(to=self.currency)
        else:
            result = Price(value=self.value + other.value, currency=self.currency)

        return result

    def __sub__(self, other: Any) -> "Price":
        if not isinstance(other, Price):
            raise ValueError("Can perform operation only with Price objects.")

        if self.currency != other.currency:
            middle_currency = "CHF"
            self_converted = self.convert(to=middle_currency)
            other_converted = other.convert(to=middle_currency)
            result = Price(
                value=self_converted.value - other_converted.value, currency=middle_currency
            ).convert(to=self.currency)
        else:
            result = Price(value=self.value - other.value, currency=self.currency)

        return result

users = {
    "admin": "password123",
    "user": "userpass",
}

auth_cache = {}

def auth(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        while True:
            username = input("Enter username: ")
            password = input("Enter password: ")

            if username in auth_cache:
                print("Authorization cached.")
                break

            if users.get(username) == password:
                print("Authorization successful.")
                auth_cache[username] = True
                break
            else:
                print("Invalid credentials. Please try again.")

        return func(*args, **kwargs)

    return wrapper

@auth
def command():
    print("Executing secured command...")

phone = Price(value=200, currency="USD")
tablet = Price(value=400, currency="USD")
watch = Price(value=300, currency="EUR")

total = phone + tablet
print(total)

difference = tablet - phone
print(difference)

total_diff_currency = phone + watch
print(total_diff_currency)

difference_diff_currency = phone - watch
print(difference_diff_currency)


command()
