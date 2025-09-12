import pandas
from numpy.ma.core import squeeze
from abc import ABC, abstractmethod  # for abstract classes

# Load CSV files
df = pandas.read_csv("hotels.csv", dtype={"id": str})
df_cards = pandas.read_csv("cards.csv", dtype=str).to_dict(orient="records")
df_security_card = pandas.read_csv("card_security.csv", dtype=str)


# -------------------
# Hotel Class
# -------------------
class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = df.loc[df["id"] == self.hotel_id, "name"].squeeze()

    def book(self):
        """Book a hotel (mark as not available)."""
        df.loc[df["id"] == self.hotel_id, "available"] = "no"
        df.to_csv("hotels.csv", index=False)

    def available(self):
        """Check if hotel is free."""
        availability = df.loc[df["id"] == self.hotel_id, "available"].squeeze()
        return availability == "yes"

    @property
    def is_big(self):
        """Check if hotel has big capacity (>= 4 people)."""
        capacity = df.loc[df["id"] == self.hotel_id, "capacity"].squeeze()
        return int(capacity) >= 4

    @classmethod
    def from_name(cls, hotel_name):
        """Create a hotel object directly from hotel name."""
        hotel_id = df.loc[df["name"] == hotel_name, "id"].squeeze()
        return cls(hotel_id)

    @staticmethod
    def hotel_exists(hotel_id):
        """Check if hotel ID exists in the dataset."""
        return hotel_id in df["id"].values

    def __eq__(self, other):
        return self.hotel_id == other.hotel_id


# -------------------
# Reservation Tickets
# -------------------
class ReservationTickets:
    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel = hotel_object

    def generate(self):
        content = f"""
        Thank you for your reservation!
        Here is your booking data:
        ----------------------------
        Name: {self.customer_name}
        Hotel name: {self.hotel.name}
        """
        return content


# -------------------
# Abstract Payment Method
# -------------------
class PaymentMethod(ABC):
    """Abstract base class for all payment methods."""

    @abstractmethod
    def validate(self, number: str, expiration: str, holder: str, cvc: str) -> bool:
        """Validate payment details."""
        pass


# -------------------
# Credit Card Classes
# -------------------
class CreditCard(PaymentMethod):
    def __init__(self, number: str):
        self.number = number

    def validate(self, number: str, expiration: str, holder: str, cvc: str) -> bool:
        card_data = {
            "number": number,
            "expiration": expiration,
            "holder": holder,
            "cvc": cvc,
        }
        return card_data in df_cards


class SecureCreditCard(CreditCard):
    def authenticate(self, given_password):
        password = df_security_card.loc[
            df_security_card["number"] == self.number, "password"
        ].squeeze()
        return password == given_password


# -------------------
# Booking Flow
# -------------------
hotel_ID = input("Add the id of the hotel: ")

if not Hotel.hotel_exists(hotel_ID):
    print("❌ Hotel with this ID does not exist.")
else:
    hotel = Hotel(hotel_ID)

    if hotel.available():
        credit_card = SecureCreditCard(number="2345675678")

        if credit_card.validate(
            expiration="08.12.2025", holder="Asen Asen", cvc="234"
        ):
            if credit_card.authenticate(given_password="mypass"):
                hotel.book()
                name = input("Enter your name: ")
                reservation_ticket = ReservationTickets(
                    customer_name=name, hotel_object=hotel
                )
                print(reservation_ticket.generate())

                print("Big hotel (capacity >= 4):", hotel.is_big)

                another_hotel = Hotel.from_name(hotel_name=hotel.name)
                print("Reservation confirmed for another hotel object:", another_hotel.name)

            else:
                print("❌ Credit card authentication failed")
        else:
            print("❌ Payment validation failed")
    else:
        print("❌ Hotel is not free")