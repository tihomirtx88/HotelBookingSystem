import pandas
from numpy.ma.core import squeeze

df = pandas.read_csv("hotels.csv", dtype={"id":str});
df_cards = pandas.read_csv("cards.csv", dtype=str).to_dict(orient="records");

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

hotel_ID = input("Add the id of the hotel: ")
hotel = Hotel(hotel_ID);

if hotel.available():
    credit_card = CreditCard( number="2345675678");
    if credit_card.validate( expiration="08.12.2025", holder="Asen Asen", cvc="234"):
        hotel.book();
        name = input("Enter your name: ");
        reservation_ticket = ReservationTickets(customer_name=name, hotel_object=hotel);
        print(reservation_ticket.generate());
    else:
        print("There is problem with payment")
else:
    print("hotel is not free");