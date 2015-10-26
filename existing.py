import sys
import cx_Oracle
import getpass
import main

def existing(email, CONN_STRING):
    sql = """select distinct tickets.tno, tickets.name, 
    to_char(bookings.dep_date), round(flight_fares.price, 2)
    from bookings, tickets, flight_fares, passengers
    where passengers.email = '{0}'
    and tickets.name = passengers.name
    and bookings.tno = tickets.tno
    and flight_fares.fare = bookings.fare
    and flight_fares.flightno = bookings.flightno""".format(email)
    existing_flights = main.sqlWithReturn(sql, CONN_STRING)
    print("Your current existing bookings are:")
    if len(existing_flights) > 0:
        counter = 1
        for row in existing_flights:
            print(str(counter) + ". ",end=""), print(row)
            counter = counter + 1
        print(str(counter) + ". Cancel one of your flights")
        counter = counter + 1
        print(str(counter) + ". Logout")
        counter = counter + 1
        print(str(counter) + ". Menu")
        print("""Enter the number in front of one of your bookings to 
see more detailed information about the booking or enter the
number in front of cancel to enter cancel mode""")
        option = input()
        if 0 < int(option) <= len(existing_flights):
            more_info(existing_flights[int(option)-1][0], CONN_STRING, email)
        elif int(option) == len(existing_flights)+1:
            cancel(existing_flights, email, CONN_STRING)
        elif int(option) == len(existing_flights)+2:
            main.init()
        elif int(option) == len(existing_flights)+3:
            main.menu(email, CONN_STRING)
        else:
            print("Invalid choice, try again")
            existing(email, CONN_STRING)
    else:
        print("You have no bookings")
        main.menu(email, CONN_STRING)

def more_info(tno, CONN_STRING, email):
    sql = """select tickets.name, tickets.email, tickets.paid_price,
    flight_fares.price, fares.fare, fares.descr, flight_fares.bag_allow,
    bookings.flightno, bookings.seat, bookings.dep_date, 
    to_char(flights.dep_time, 'HH24:MI'), flights.est_dur, flights.src, 
    a1.name, a1.city, a1.country, a1.tzone, flights.dst, a2.name, a2.city, 
    a2.country, a2.tzone
    from tickets, flight_fares, fares, bookings, flights, airports a1,
    airports a2
    where tickets.tno = {0}
    and bookings.tno = tickets.tno
    and flight_fares.fare = bookings.fare
    and flight_fares.flightno = bookings.flightno
    and fares.fare = flight_fares.fare
    and flights.flightno = bookings.flightno
    and a1.acode = flights.src
    and a2.acode = flights.dst
    """.format(tno)
    info, column = main.sqlWithReturnColumn(sql, CONN_STRING)
    for row in info:
        for index in range(0, len(row)):
            print(column[index][0] + ': ', end=""), print(row[index])
    main.menu(email, CONN_STRING)

def cancel(existing_flights, email, CONN_STRING):
    print("Enter the number of the row you would like to delete")
    option = input()
    if 0 < int(option) <= len(existing_flights):
        tno = existing_flights[int(option)-1][0]
        deleteFromBookings = """delete from bookings
        where tno = {0}
	""".format(tno)
	main.sqlWithNoReturn(deleteFromBookings, CONN_STRING)
        deleteFromTickets = """delete from tickets
        where tno = {0}
        """.format(tno)
	main.sqlWithNoReturn(deleteFromTickets, CONN_STRING)
    elif int(option) == len(existing_flights)+1:
        cancel(existing_flights, email)
    elif int(option) == len(existing_flights)+2:
        main.init()
    elif int(option) == len(existing_flights)+3:
        main.menu(email, CONN_STRING)
    else:
        print("Invalid choice")
        existing(email, CONN_STRING)    
    main.menu(email, CONN_STRING)

#user = input("User: ")
#pwd = getpass.getpass()
#CONN_STRING = '' + user + '/' + pwd + '@gwynne.cs.ualberta.ca:1521/CRS'
#existing("davood@ggg.com", CONN_STRING)
