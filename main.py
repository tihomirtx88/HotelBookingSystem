import pandas
from numpy.ma.core import squeeze

df = pandas.read_csv("hotels.csv", dtype={"id":str});

class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id;

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
        pass;

    def generate(self):
        pass;

print(df)

hotel_ID = input("Add the id of the hotel: ")
hotel = Hotel(hotel_ID);

if hotel.available():
    hotel.book();
    name = input("Enter your name: ");
    reservation_ticket = ReservationTickets(name, hotel);
    print(reservation_ticket.generate());
else:
    print("hotel is not free");