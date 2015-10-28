import sys
import cx_Oracle
import getpass
import main

# displays the existing bookings for the current user and gives them options of
# what to do
def existing(email, CONN_STRING):
    # sql command to display all of the bookings for the current user
    sql = """select distinct tickets.tno, tickets.name, 
    to_char(bookings.dep_date), round(flight_fares.price, 2)
    from bookings, tickets, flight_fares, passengers
    where passengers.email = '{0}'
    and tickets.name = passengers.name
    and bookings.tno = tickets.tno
    and flight_fares.fare = bookings.fare
    and flight_fares.flightno = bookings.flightno""".format(email)
    
    # see if the command can execute
    try:
        existing_flights = main.sqlWithReturn(sql, CONN_STRING)
    except:
        # if it can't tell the user and return to the main menu
        print("Something has gone wrong while trying to display your bookings")
        return main.menu(email, CONN_STRING)
        
    # if it can, print them for the user
    if len(existing_flights) > 0:
        print("Your current existing bookings are:")
        # the counter is used to display the numbers next to each row that the
        # user will use to indicate which row they'd like to select
        counter = 1
        # print a number, followed by one of the rows for each row
        for row in existing_flights:
            print(str(counter) + ". ",end=""), print(row)
            counter = counter + 1
        # print the option to go into cancel mode
        print(str(counter) + ". Cancel one of your flights")
        counter = counter + 1
        # print the option to go back to the menu
        print(str(counter) + ". Menu")
        
        # prompt the user to select an option
        print("""Enter the number in front of one of your bookings to 
see more detailed information about the booking or enter the
number in front of cancel to enter cancel mode""")
        # record their selection
        option = input()
        
        try:
            option = int(option)
        except:
            print('Your selection must be one of the integers listed above')
            return existing(email, CONN_STRING)
        
        # if they selected one of the row numbers, print more information about
        # that booking
        if 0 < option <= len(existing_flights):
            return more_info(existing_flights[int(option)-1][0], CONN_STRING, email)
        # if they selected the cancel option, call the cancel function
        elif option == len(existing_flights)+1:
            return cancel(existing_flights, email, CONN_STRING)
        # if they selected the menu, go to the menu 
        elif option == len(existing_flights)+2:
            return main.menu(email, CONN_STRING)
        # if they did not select one of the options above, it is an invalid 
        # choice
        else:
            print("Invalid choice, try again")
            return existing(email, CONN_STRING)
    # tell the user if they have no flights    
    else:
        print("You have no bookings")
        return main.menu(email, CONN_STRING)

# presents all info about a booking the user selects and returns it to the
# menu
def more_info(tno, CONN_STRING, email):
    # sql command to obtain all information about a booking
    sql = """select tickets.name, tickets.email, tickets.paid_price,
    flight_fares.price, fares.fare, fares.descr, flight_fares.bag_allow,
    bookings.flightno, bookings.seat, bookings.dep_date, 
    to_char(flights.dep_time, 'HH24:MI') as Dep_time, flights.est_dur, flights.src, 
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
    
    # try to execute the command
    try:
        info, column = main.sqlWithReturnDesc(sql, CONN_STRING)
    except:
        # if it doesn't work, tell the user
        print("Something has gone wrong with accessing the requested info")
        return main.menu(email, CONN_STRING)
    # if it does, print all of the information and go back to the menu
    for row in info:
        for index in range(0, len(row)):
            print(column[index][0] + ': ', end=""), print(row[index])
    return main.menu(email, CONN_STRING)

# a mode in which the user can select one of their displayed bookings to cancel
def cancel(existing_flights, email, CONN_STRING):
    # get the number of the row that the user would like to delete
    print("Enter the number of the row you would like to delete")
    option = input()
    
    # see if they entered a number
    try:
        option = int(option)
    except:
        print("You must enter one of the integers next to the desired option")
        return existing(email, CONN_STRING)
    
    # if they select a row number, delete the rows
    if 0 < option <= len(existing_flights):
        tno = existing_flights[int(option)-1][0]
        deleteFromBookings = """delete from bookings
        where tno = {0}
	""".format(tno)
        try:
            main.sqlWithNoReturn(deleteFromBookings, CONN_STRING)
        except:
            print("Could not delete your booking")
            return main.menu(email, CONN_STRING)
        deleteFromTickets = """delete from tickets
        where tno = {0}
        """.format(tno)
        try:
            main.sqlWithNoReturn(deleteFromTickets, CONN_STRING)
        except:
            print("Could not delete your ticket")
            return main.menu(email, CONN_STRING)
        print("Successfully deleted booking and ticket")
    # if they select the cancel option again, run cancel again
    elif option == len(existing_flights)+1:
        return cancel(existing_flights, email, CONN_STRING)
    # if they select the menu option, go to the menu
    elif option == len(existing_flights)+2:
        return main.menu(email, CONN_STRING)
    # if it's not one of the above options, it's invalid, tell them    
    else:
        print("Invalid choice")
        return existing(email, CONN_STRING)    
    main.menu(email, CONN_STRING)

