import main
import search

# prompt user for information of a round trip and call printRoundInfo
# to search for suitable flights
def roundTrip(email, CONN_STRING):
    source = input("Source: ").upper()
    dest = input("Destination: ").upper()
    dep_date = input("Departure Date (DD/MM/YYYY): ")
    ret_date = input("Return Date (DD/MM/YYYY): ")
    printRoundInfo(email, CONN_STRING, source, dest, dep_date, ret_date)

# use user entered information to find suitable flights. display the
# information and provide users with options of sorting the results
# in number of connections, make a booking and go back to main menu
def printRoundInfo(email, CONN_STRING, source, dest, dep_date, ret_date, sortBy="1"):
    # query that selects suitable round trip flights sorted by price and
    # airport code
    sortByPrice = """
    select t1.flightno1, t1.flightno2, t1.src, t1.dst, t1.dep_date, 
           t1.dep_time, t1.arr_time, t1.layover, t1.fare1,
           t1.fare2, t2.flightno1 as flightno3, t2.flightno2 as flightno4,
           t2.dep_date as ret_date, t2.dep_time, t2.arr_time,
           t2.layover, t2.fare1 as fare3, t2.fare2 as fare4, 
           t1.stops + t2.stops as stops,
           (t1.seats + t2.seats) / 2 - abs(t1.seats - t2.seats) / 2 as seats,
           t1.price + t2.price as price
    from
    (select flightno1, flightno2, src, dst, to_char(dep_date) as dep_date,
           to_char(dep_time, 'HH24:MI') as dep_time,
           to_char(arr_time, 'HH24:MI') as arr_time,
           stops, 60 * layover as layover
           , price, fare1, fare2,
           (seats1 + seats2) / 2 - abs(seats1 - seats2) / 2 as seats
    from
    (select flightno1, flightno2, src, dst, dep_time, arr_time,
          1 stops, layover, price, seats1, seats2, dep_date, fare1, fare2
    from good_connections
    where to_char(dep_date,'DD/MM/YYYY')='{2}' and src='{0}' and dst='{1}'
    union
    select flightno flightno1, '' flightno2, src, dst, dep_time,
          arr_time, 0 stops, 0 layover, price, seats seats1,
          seats+1 as seats2, dep_date, fare as fare1, null fare2
    from available_flights
    where to_char(dep_date,'DD/MM/YYYY')='{2}' and src='{0}' and dst='{1}'
    order by price asc)) t1,
    (select flightno1, flightno2, src, dst, to_char(dep_date) as dep_date,
           to_char(dep_time, 'HH24:MI') as dep_time,
           to_char(arr_time, 'HH24:MI') as arr_time,
           stops, 60 * layover as layover
           , price, fare1, fare2,
           (seats1 + seats2) / 2 - abs(seats1 - seats2) / 2 as seats
    from
    (select flightno1, flightno2, src, dst, dep_time, arr_time,
          1 stops, layover, price, seats1, seats2, dep_date, fare1, fare2
    from good_connections
    where to_char(dep_date,'DD/MM/YYYY')='{3}' and src='{1}' and dst='{0}'
    union
    select flightno flightno1, '' flightno2, src, dst, dep_time,
          arr_time, 0 stops, 0 layover, price, seats seats1,
          seats+1 as seats2, dep_date, fare as fare1, null fare2
    from available_flights
    where to_char(dep_date,'DD/MM/YYYY')='{3}' and src='{1}' and dst='{0}'
    order by price asc)) t2
    order by price asc
    """.format(source, dest, dep_date, ret_date)
    # query that selects suitable round trip flights sorted by first stops
    # then price and airport code
    sortByStops = """
    select t1.flightno1, t1.flightno2, t1.src, t1.dst, t1.dep_date, 
           t1.dep_time, t1.arr_time, t1.layover, t1.fare1,
           t1.fare2, t2.flightno1 as flightno3, t2.flightno2 as flightno4,
           t2.dep_date as ret_date, t2.dep_time, t2.arr_time,
           t2.layover, t2.fare1 as fare3, t2.fare2 as fare4, 
           t1.stops + t2.stops as stops,
           (t1.seats + t2.seats) / 2 - abs(t1.seats - t2.seats) / 2 as seats,
           t1.price + t2.price as price
    from
    (select flightno1, flightno2, src, dst, to_char(dep_date) as dep_date,
           to_char(dep_time, 'HH24:MI') as dep_time,
           to_char(arr_time, 'HH24:MI') as arr_time,
           stops, 60 * layover as layover
           , price, fare1, fare2,
           (seats1 + seats2) / 2 - abs(seats1 - seats2) / 2 as seats
    from
    (select flightno1, flightno2, src, dst, dep_time, arr_time,
          1 stops, layover, price, seats1, seats2, dep_date, fare1, fare2
    from good_connections
    where to_char(dep_date,'DD/MM/YYYY')='{2}' and src='{0}' and dst='{1}'
    union
    select flightno flightno1, '' flightno2, src, dst, dep_time,
          arr_time, 0 stops, 0 layover, price, seats seats1,
          seats+1 as seats2, dep_date, fare as fare1, null fare2
    from available_flights
    where to_char(dep_date,'DD/MM/YYYY')='{2}' and src='{0}' and dst='{1}'
    order by price asc)) t1,
    (select flightno1, flightno2, src, dst, to_char(dep_date) as dep_date,
           to_char(dep_time, 'HH24:MI') as dep_time,
           to_char(arr_time, 'HH24:MI') as arr_time,
           stops, 60 * layover as layover
           , price, fare1, fare2,
           (seats1 + seats2) / 2 - abs(seats1 - seats2) / 2 as seats
    from
    (select flightno1, flightno2, src, dst, dep_time, arr_time,
          1 stops, layover, price, seats1, seats2, dep_date, fare1, fare2
    from good_connections
    where to_char(dep_date,'DD/MM/YYYY')='{3}' and src='{1}' and dst='{0}'
    union
    select flightno flightno1, '' flightno2, src, dst, dep_time,
          arr_time, 0 stops, 0 layover, price, seats seats1,
          seats+1 as seats2, dep_date, fare as fare1, null fare2
    from available_flights
    where to_char(dep_date,'DD/MM/YYYY')='{3}' and src='{1}' and dst='{0}'
    order by price asc)) t2
    order by stops, price asc
    """.format(source, dest, dep_date, ret_date)

    # use the corresponding query to sort the result
    if sortBy == "1":
        try:
            rs, desc = main.sqlWithReturnDesc(sortByPrice, CONN_STRING)
        except:
            print("no match found")
            return printRoundInfo(email, CONN_STRING, source, dest, dep_date, ret_date, "1")
    else:
        try:
            rs, desc = main.sqlWithReturnDesc(sortByStops, CONN_STRING)
        except:
            print("no match found")
            return printRoundInfo(email, CONN_STRING, source, dest, dep_date, ret_date, "1")

    # if there is result print column name and rows
    if len(rs) != 0:
        i = 1
        for row in desc:
            print(row[0], end=" ")
        print("")
        for row in rs:
            print(str(i)+".",row)
            i+=1
    # if no result then use implicit search
    else:
        # query that selects suitable round trip flights sorted by price and
        # similar aiport name or city name
        sortByPrice = """
        select t1.flightno1, t1.flightno2, t1.src, t1.dst, t1.dep_date, 
           t1.dep_time, t1.arr_time, t1.layover, t1.fare1,
           t1.fare2, t2.flightno1 as flightno3, t2.flightno2 as flightno4,
           t2.dep_date as ret_date, t2.dep_time, t2.arr_time,
           t2.layover, t2.fare1 as fare3, t2.fare2 as fare4, 
           t1.stops + t2.stops as stops,
           (t1.seats + t2.seats) / 2 - abs(t1.seats - t2.seats) / 2 as seats,
           t1.price + t2.price as price
        from airports a1, airports a2,
        (select flightno1, flightno2, src, dst, to_char(dep_date) as dep_date,
           to_char(dep_time, 'HH24:MI') as dep_time,
           to_char(arr_time, 'HH24:MI') as arr_time,
           stops, 60 * layover as layover
           , price, fare1, fare2,
           (seats1 + seats2) / 2 - abs(seats1 - seats2) / 2 as seats
        from
        (select flightno1, flightno2, src, dst, dep_time, arr_time,
          1 stops, layover, price, seats1, seats2, dep_date, fare1, fare2
        from good_connections
        where to_char(dep_date,'DD/MM/YYYY')='{2}'
        union
        select flightno flightno1, '' flightno2, src, dst, dep_time,
        arr_time, 0 stops, 0 layover, price, seats seats1,
          seats+1 as seats2, dep_date, fare as fare1, null fare2
        from available_flights
        where to_char(dep_date,'DD/MM/YYYY')='{2}'
        order by price asc)) t1,
        (select flightno1, flightno2, src, dst, to_char(dep_date) as dep_date,
           to_char(dep_time, 'HH24:MI') as dep_time,
           to_char(arr_time, 'HH24:MI') as arr_time,
           stops, 60 * layover as layover
           , price, fare1, fare2,
           (seats1 + seats2) / 2 - abs(seats1 - seats2) / 2 as seats
        from
        (select flightno1, flightno2, src, dst, dep_time, arr_time,
          1 stops, layover, price, seats1, seats2, dep_date, fare1, fare2
        from good_connections
        where to_char(dep_date,'DD/MM/YYYY')='{3}'
        union
        select flightno flightno1, '' flightno2, src, dst, dep_time,
          arr_time, 0 stops, 0 layover, price, seats seats1,
          seats+1 as seats2, dep_date, fare as fare1, null fare2
        from available_flights
        where to_char(dep_date,'DD/MM/YYYY')='{3}'
        order by price asc)) t2
        where (lower(t1.src) = '{0}' and a1.acode = t1.src or
              (t1.src = a1.acode and lower(a1.city) like '%{0}%'
              or lower(a1.name) like '%{0}%'))
              and
              (lower(t1.dst) = '{1}' and a2.acode = t1.dst or
              (t1.dst = a2.acode and lower(a2.city) like '%{1}%'
              or lower(a2.name) like '%{1}%'))
              and t1.src = t2.dst and t1.dst = t2.src
        order by price asc
        """.format(source.lower(), dest.lower(), dep_date, ret_date)
        # query that selects suitable round trip flights sorted by stops
        # then price and similar aiport name or city name
        sortByStops = """
        select t1.flightno1, t1.flightno2, t1.src, t1.dst, t1.dep_date, 
           t1.dep_time, t1.arr_time, t1.layover, t1.fare1,
           t1.fare2, t2.flightno1 as flightno3, t2.flightno2 as flightno4,
           t2.dep_date as ret_date, t2.dep_time, t2.arr_time,
           t2.layover, t2.fare1 as fare3, t2.fare2 as fare4, 
           t1.stops + t2.stops as stops,
           (t1.seats + t2.seats) / 2 - abs(t1.seats - t2.seats) / 2 as seats,
           t1.price + t2.price as price
        from airports a1, airports a2,
        (select flightno1, flightno2, src, dst, to_char(dep_date) as dep_date,
           to_char(dep_time, 'HH24:MI') as dep_time,
           to_char(arr_time, 'HH24:MI') as arr_time,
           stops, 60 * layover as layover
           , price, fare1, fare2,
           (seats1 + seats2) / 2 - abs(seats1 - seats2) / 2 as seats
        from
        (select flightno1, flightno2, src, dst, dep_time, arr_time,
          1 stops, layover, price, seats1, seats2, dep_date, fare1, fare2
        from good_connections
        where to_char(dep_date,'DD/MM/YYYY')='{2}'
        union
        select flightno flightno1, '' flightno2, src, dst, dep_time,
        arr_time, 0 stops, 0 layover, price, seats seats1,
          seats+1 as seats2, dep_date, fare as fare1, null fare2
        from available_flights
        where to_char(dep_date,'DD/MM/YYYY')='{2}'
        order by price asc)) t1,
        (select flightno1, flightno2, src, dst, to_char(dep_date) as dep_date,
           to_char(dep_time, 'HH24:MI') as dep_time,
           to_char(arr_time, 'HH24:MI') as arr_time,
           stops, 60 * layover as layover
           , price, fare1, fare2,
           (seats1 + seats2) / 2 - abs(seats1 - seats2) / 2 as seats
        from
        (select flightno1, flightno2, src, dst, dep_time, arr_time,
          1 stops, layover, price, seats1, seats2, dep_date, fare1, fare2
        from good_connections
        where to_char(dep_date,'DD/MM/YYYY')='{3}'
        union
        select flightno flightno1, '' flightno2, src, dst, dep_time,
          arr_time, 0 stops, 0 layover, price, seats seats1,
          seats+1 as seats2, dep_date, fare as fare1, null fare2
        from available_flights
        where to_char(dep_date,'DD/MM/YYYY')='{3}'
        order by price asc)) t2
        where (lower(t1.src) = '{0}' and a1.acode = t1.src or
              (t1.src = a1.acode and lower(a1.city) like '%{0}%'
              or lower(a1.name) like '%{0}%'))
              and
              (lower(t1.dst) = '{1}' and a2.acode = t1.dst or
              (t1.dst = a2.acode and lower(a2.city) like '%{1}%'
              or lower(a2.name) like '%{1}%'))
              and t1.src = t2.dst and t1.dst = t2.src
        order by stops, price asc
        """.format(source.lower(), dest.lower(), dep_date, ret_date)
        if sortBy == "1":
            rs, desc = main.sqlWithReturnDesc(sortByPrice, CONN_STRING)
        else:
            rs, desc = main.sqlWithReturnDesc(sortByStops, CONN_STRING)
        # print searching result if exists
        if len(rs) != 0:
            i = 1
            for row in desc:
                print(row[0], end=" ")
            print("")
            for row in rs:
                print(str(i)+".", row)
                i+=1
        # print error message and go back to menu
        else:
            print("no results")
            return main.menu(email, CONN_STRING)

    # print options
    print(str(len(rs)+1)+".", "Sort by number of connections")
    print(str(len(rs)+2)+".", "Make a booking")
    print(str(len(rs)+3)+".", "Go back to menu")

    # get options and call corresponding method
    option = input("Enter the number of an option: ")
    try:
        optNum = int(option)
        if optNum<0 or optNum>len(rs)+3:
            print("Not valid number")
        elif optNum == len(rs)+1:
            return printRoundInfo(email, CONN_STRING, source, dest, dep_date, ret_date, "2")
        elif optNum == len(rs)+2:
            # get user selected number of flight
            flightno = int(input("Enter the number before the flight you want to book: "))
            # go back to start of function if flightno is less than one
            # to prevent negative indexing issues
            if flightno < 1:
                return printRoundInfo(email, CONN_STRING, source, dest, dep_date, ret_date, sortBy)
                
            # get a new result set of current data
            if sortBy == "1":
                newRs = main.sqlWithReturn(sortByPrice, CONN_STRING)
            else:
                newRs = main.sqlWithReturn(sortByStops, CONN_STRING)

            # compare each row in new result set with user selected row and
            # record the index
            selected = rs[flightno-1]
            i = 0
            for row in newRs:
                if row[0] == selected[0] and row[1] == selected[1] and row[8] == selected[8] and row[9] == selected[9] and row[10] == selected[10] and row[11] == selected[11] and row[-5] == selected[-5] and row[-4] == selected[-4]:
                    break
                else:
                    i += 1
            # if not found, print error message and go back
            if i == len(newRs):
                print("tickets for your selected flight has run out")
                return printRoundInfo(email, CONN_STRING, source, dest, dep_date, ret_date, sortBy)
            # call booking function
            return roundBooking(email, CONN_STRING, i+1, newRs, dep_date, ret_date, source, dest)
        elif optNum == len(rs)+3:
            return main.menu(email, CONN_STRING)
        else:
            print("Not valid number")
            return printRoundInfo(email, CONN_STRING, source, dest, dep_date, ret_date, sortBy)
    except:
        print("Not valid number")
        return printRoundInfo(email, CONN_STRING, source, dest, dep_date, ret_date, sortBy)

# allow the user to make a booking for selected flight. prompt user 
# for passenger information if user is not registered in passenger
# table
def roundBooking(email, CONN_STRING, flightno, rs, dep_date, ret_date, source, dest):

    # if user is not a passenger prompt user to enter information
    # and add it to passenger table
    sql = "select * from passengers where email = '{0}'".format(email)
    isPassenger = main.sqlWithReturn(sql, CONN_STRING)
    if len(isPassenger) == 0:
        print("You are currently not a passenger. Please enter the information below.")
        name = input("Name: ")
        country = input("Country: ")
        sql = "insert into passengers values('{0}', '{1}', '{2}')".format(email, name, country)
        main.sqlWithNoReturn(sql, CONN_STRING)
    row = rs[flightno-1]

    # get ticket number to be created
    sql = "select max(tno) from tickets"
    maxTno = main.sqlWithReturn(sql, CONN_STRING)[0][0]
    # get name of passenger
    sql = "select name from passengers where email = '{0}'".format(email)
    name = main.sqlWithReturn(sql, CONN_STRING)[0][0]
    # create a ticker for this purchase
    sql = "insert into tickets values({0}, '{1}', '{2}', '{3}')".format(maxTno+1, name, email, row[-1])
    main.sqlWithNoReturn(sql, CONN_STRING)
    # record the first flight booking information
    sql = "insert into bookings values({0}, '{1}', '{2}', to_date('{3}', 'DD/MM/YYYY'), null)".format(maxTno+1, row[0], row[8], dep_date)
    main.sqlWithNoReturn(sql, CONN_STRING)
    # record the first return flight booking information
    sql = "insert into bookings values({0}, '{1}', '{2}', to_date('{3}', 'DD/MM/YYYY'), null)".format(maxTno+1, row[10], row[-5], ret_date)
    main.sqlWithNoReturn(sql, CONN_STRING)
    # record the second booking information if there is one
    if row[1] is not None:
        sql = "insert into bookings values({0}, '{1}', '{2}', to_date('{3}', 'DD/MM/YYYY'), null)".format(maxTno+1, row[1], row[9], dep_date)
        main.sqlWithNoReturn(sql, CONN_STRING)
    # record the second return booking information if there is one
    if row[11] is not None:
        sql = "insert into bookings values({0}, '{1}', '{2}', to_date('{3}', 'DD/MM/YYYY'), null)".format(maxTno+1, row[11], row[-4], ret_date)
        main.sqlWithNoReturn(sql, CONN_STRING)
    # print success message and ticket number and go back
    print("success, your ticket number is ", maxTno+1)
    return printRoundInfo(email, CONN_STRING, source, dest, dep_date, ret_date)
