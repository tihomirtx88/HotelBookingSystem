import pandas
from numpy.ma.core import squeeze

df = pandas.read_csv("hotels.csv", dtype={"id":str});
df_cards = pandas.read_csv("cards.csv", dtype=str).to_dict(orient="records");
df_security_card = pandas.read_csv("card_security.csv", dtype=str);

class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id;
        self.name = df.loc[df["id"] == self.hotel_id, "name"].squeeze();

    def book(self):
        # Book hotel
        df.loc[df["id"] == self.hotel_id, "available"] = "no";
        df.to_csv("hotels.csv", index=False);

    def available(self):
        # Checks hotel is free
        availability = df.loc[df["id"] == self.hotel_id, "available"].squeeze();
        if availability == "yes":
            return True;
        else:
            return False;

    @property
    def is_big(self):
        """Check if hotel has big capacity (>= 4 people)."""
        capacity = df.loc[df["id"] == self.hotel_id, "capacity"].squeeze();
        return int(capacity) >= 4;

    @classmethod
    def from_name(cls, hotel_name):
        """Create a hotel object directly from hotel name."""
        hotel_id = df.loc[df["name"] == hotel_name, "id"].squeeze();
        return cls(hotel_id);

    @staticmethod
    def hotel_exists(hotel_id):
        """Check if hotel ID exists in the dataset."""
        return hotel_id in df["id"].values

    def __eq__(self, other):
        if self.hotel_id == other.hotel_id:
            return True
        else:
            return False;

class ReservationTickets:
    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name;
        self.hotel = hotel_object;

    def generate(self):
        conten = f"""
        Thank you for your reservation
        Here you are booking data:
        Name: {self.customer_name}
        Hotel name: {self.hotel.name}
        """
        return conten;

class CreditCard:
    def __init__(self, number):
        self number = number;

    def validate(self, expiration, holder, cvc):
        cad_data = {"number": self.number, "expiration": expiration, "holder": holder, "cvc": cvc};
        if cad_data in df_cards:
            return True;
        else:
            return False;

# Inheritance
class SecureCreditCard(CreditCard):
    def authenticate(self, given_password):
        password = df_security_card.loc[df_security_card["number"] == self.number, "password"].squeeze();

        if password == given_password:
            return  True;
        else:
            return False;

hotel_ID = input("Add the id of the hotel: ")
if not Hotel.hotel_exists(hotel_ID):
    print("❌ Hotel with this ID does not exist.")
else:
    hotel = Hotel(hotel_ID);

    if hotel.available():
        credit_card = SecureCreditCard( number="2345675678");
        if credit_card.validate( expiration="08.12.2025", holder="Asen Asen", cvc="234"):
            if credit_card.authenticate(given_password="mypass")
                hotel.book();
                name = input("Enter your name: ");
                reservation_ticket = ReservationTickets(customer_name=name, hotel_object=hotel);
                print(reservation_ticket.generate());

                print("Big hotel (capacity >= 4):", hotel.is_big);

                another_hotel = Hotel.from_name(hotel_name=hotel.name);
            else:
                print("Credit card authentication falied")
        else:
            print("There is problem with payment")
    else:
        print("hotel is not free");