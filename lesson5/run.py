from typing import NamedTuple, Any

CURRENCY_TO_CHF = {
    "USD": 0.91,
    "EUR": 1.08,
    "CHF": 1.0
}

CHF_TO_CURRENCY = {currency: 1 / rate for currency, rate in CURRENCY_TO_CHF.items()}

class Price:
    def __init__(self, value: float, currency: str):
        if currency not in CURRENCY_TO_CHF:
            raise ValueError(f"Unsupported currency: {currency}")

        self.value = value
        self.currency = currency

    def __add__(self, other: Any) -> "Price":
        if not isinstance(other, Price):
            raise TypeError("Can only add Price instances")

        if self.currency == other.currency:
            return Price(self.value + other.value, self.currency)

        converted_value = (self.to_chf().value + other.to_chf().value) * CHF_TO_CURRENCY[self.currency]
        return Price(converted_value, self.currency)

    def __sub__(self, other: Any) -> "Price":
        if not isinstance(other, Price):
            raise TypeError("Can only subtract Price instances")

        if self.currency == other.currency:
            return Price(self.value - other.value, self.currency)

        converted_value = (self.to_chf().value - other.to_chf().value) * CHF_TO_CURRENCY[self.currency]
        return Price(converted_value, self.currency)

    def to_chf(self) -> "Price":
        return Price(self.value * CURRENCY_TO_CHF[self.currency], "CHF")

    def __repr__(self) -> str:
        return f"Price({self.value:.2f}, \"{self.currency}\")"

a = Price(100, "USD")
b = Price(200, "EUR")

print(a + b)
print(a - b)

from functools import wraps

users = {
    "user1": "password1",
    "admin": "admin123"
}

authenticated_users = set()

def auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        global authenticated_users

        username = input("Enter username: ")
        if username in authenticated_users:
            print("User already authenticated.")
            return func(*args, **kwargs)

        while True:
            password = input("Enter password: ")
            if users.get(username) == password:
                print("Authentication successful.")
                authenticated_users.add(username)
                return func(*args, **kwargs)
            else:
                print("Invalid credentials. Try again.")
    
    return wrapper

@auth
def command():
    print("Executing command...")


command()
