import sys
import cx_Oracle
import getpass
from main import *

def existing(email):
    sql = """select tickets.tno, tickets.name, bookings.dep_date, 
    flight_fares.price
    from bookings, tickets, flight_fares, passengers
    where passengers.email = '""" + email + """'
    and tickets.name = passengers.name
    and bookings.tno = tickets.tno
    and flight_fares.fare = bookings.fare;"""
    existing_flights = sqlWithReturn(sql)
    print "Your current existing bookings are:"
    if len(existing_flights > 0):
        counter = 1;
        for row in existing_flights:
            print counter + ". " + row
            counter = counter + 1
        print counter + ". Cancel one of your flights"
        counter = counter + 1
        print counter + ". Logout"
        print """Enter the number in front of one of your bookings to 
        see more detailed information about the booking or enter the
        number in front of cancel to enter cancel mode"""
        option = input()
        if 0 < option <= len(existing_flights):
            more_info(existing_flights[option-1])
        elif option == len(existing_flights)+1:
            cancel()
        elif option == len(existing_flights)+2:
            init()
        else:
            print "Invalid choice, try again"
            existing()
    else:
        print "You have no bookings"
        menu(email)
    return
