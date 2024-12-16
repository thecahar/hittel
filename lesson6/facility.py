
import random
import string

class Product:
    def __init__(self, name: str, price: int) -> None:
        self.name: str = name
        self.price: int = price

    def __str__(self) -> str:
        return f"{self.name}: {self.price}"

    def __repr__(self) -> str:
        return "Hello there!!!"


class PdfGenerator:
    def generate_pdf(self, name: str):
        print(f"Generating PDF: {name}.pdf")

    def create_order_document(self, name: str):
        print(f"Generating PDF: {name}.pdf")


class Legals(PdfGenerator):
    def create_order_documents(self, product: Product):
        print(f"preparing documents for {product}")
        super().create_order_document(product.name)


class Delivery:
    def ship(self, product: Product):
        print(f"Shipping the product: {product.name} with {id(self)}")


class Facility:
    def __init__(self, delivery_service: Delivery, legals_service: Legals):
        self.delivery_service = delivery_service
        self.legals_service = legals_service

    def build(self) -> Product:
        random_name: str = "".join(
            [random.choice(string.ascii_letters) for _ in range(10)]
        )
        random_price: int = random.randint(10, 20)
        print(f"building product with {self.__class__.__name__}")

        return Product(name=random_name, price=random_price)


class TeslaFacility(Facility):
    pass


class IntelFacility(Facility):
    pass


delivery_service = Delivery()
legals_service = Legals()

tesla_in_california = TeslaFacility(
    delivery_service=delivery_service,
    legals_service=legals_service,
)
intel_in_california = IntelFacility(
    delivery_service=delivery_service,
    legals_service=legals_service,
)

tesla = tesla_in_california.build()
tesla_in_california.legals_service.create_order_document(tesla.name)
tesla_in_california.delivery_service.ship(tesla)

print("=" * 20)

intel = intel_in_california.build()
intel_in_california.legals_service.create_order_document(intel.name)
intel_in_california.delivery_service.ship(intel)