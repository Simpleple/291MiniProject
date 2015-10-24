import main

def printInfo(email, CONN_STRING, source, dest, dep_date, sortBy="1"):
    sortByPrice = """
    select flightno1, flightno2, src, dst, to_char(dep_time),
           to_char(arr_time), stops, 60 * layover, price, seats1, seats2
    from 
    (select flightno1, flightno2, src, dst, dep_time, arr_time,
          1 stops, layover, price, seats1, seats2
    from good_connections
    where to_char(dep_date,'DD/MM/YYYY')='{2}' and src='{0}' and dst='{1}'
    union
    select flightno flightno1, '' flightno2, src, dst, dep_time,
          arr_time, 0 stops, 0 layover, price, seats seats1, 0 seats2
    from available_flights
    where to_char(dep_date,'DD/MM/YYYY')='{2}' and src='{0}' and dst='{1}'
    order by price asc)
    """.format(source, dest, dep_date)
    sortByStops = """
    select flightno1, flightno2, src, dst, to_char(dep_time),
           to_char(arr_time), stops, 60 * layover, price, seats1, seats2
    from 
    (select flightno1, flightno2, src, dst, dep_time, arr_time,
          1 stops, layover, price, seats1, seats2
    from good_connections
    where to_char(dep_date,'DD/MM/YYYY')='{2}' and src='{0}' and dst='{1}'
    union
    select flightno flightno1, '' flightno2, src, dst, dep_time,
          arr_time, 0 stops, 0 layover, price, seats seats1, 0 seats2
    from available_flights
    where to_char(dep_date,'DD/MM/YYYY')='{2}' and src='{0}' and dst='{1}'
    order by stops, price asc)
    """.format(source, dest, dep_date)

    if sortBy == "1":
        rs = main.sqlWithReturn(sortByPrice, CONN_STRING)
    else:
        rs = main.sqlWithReturn(sortByStops, CONN_STRING)
    if len(rs) != 0:
        i = 1
        for row in rs:
            print(i," ",row)
            i+=1
    else:
        sortByPrice = """
        select x.flightno1, x.flightno2, x.src, x.dst, to_char(x.dep_time),
               to_char(x.arr_time), x.stops, 24 * x.layover, x.price, x.seats1,
               x.seats2
        from airports a1, airports a2,
            (select flightno1, flightno2, src, dst, dep_time, arr_time,
            stops, layover, price, seats1, seats2
            from 
            (select flightno1, flightno2, src, dst, dep_time, arr_time,
            1 stops, layover, price, seats1, seats2
            from good_connections
            where to_char(dep_date,'DD/MM/YYYY')='{2}'
            union
            select flightno flightno1, '' flightno2, src, dst, dep_time,
            arr_time, 0 stops, 0 layover, price, seats seats1, null seats2
            from available_flights
            where to_char(dep_date,'DD/MM/YYYY')='{2}')) x
        where (lower(a1.city) like '%{0}%'
              or lower(a1.name) like '%{0}%')
              and a1.acode = x.src and a2.acode = x.dst
              and (lower(a2.city) like '%{1}%' or 
              lower(a2.name) like '%{1}%')
        order by price asc
        """.format(source.lower(), dest.lower(), dep_date)
        sortByStops = """
        select x.flightno1, x.flightno2, x.src, x.dst, to_char(x.dep_time),
               to_char(x.arr_time), x.stops, 24 * x.layover, x.price, x.seats1,
               x.seats2
        from airports a1, airports a2,
            (select flightno1, flightno2, src, dst, dep_time, arr_time,
            stops, layover, price, seats1, seats2
            from 
            (select flightno1, flightno2, src, dst, dep_time, arr_time,
            1 stops, layover, price, seats1, seats2
            from good_connections
            where to_char(dep_date,'DD/MM/YYYY')='{2}'
            union
            select flightno flightno1, '' flightno2, src, dst, dep_time,
            arr_time, 0 stops, 0 layover, price, seats seats1, null seats2
            from available_flights
            where to_char(dep_date,'DD/MM/YYYY')='{2}')) x
        where (lower(a1.city) like '%{0}%'
              or lower(a1.name) like '%{0}%')
              and a1.acode = x.src and a2.acode = x.dst
              and (lower(a2.city) like '%{1}%' or 
              lower(a2.name) like '%{1}%')
        order by stops, price asc
        """.format(source.lower(), dest.lower(), dep_date)
        if sortBy == "1":
            rs = main.sqlWithReturn(sortByPrice, CONN_STRING)
        else:
            rs = main.sqlWithReturn(sortByStops, CONN_STRING)
        if len(rs) != 0:
            i = 1
            for row in rs:
                print(i, " ", row)
                i+=1
        else:
            print("no results")
    print(len(rs)+1, " ", "Sort by number of connections")
    print(len(rs)+2, " ", "Make a booking")
    print(len(rs)+3, " ", "Go back to menu")
    print(len(rs)+4, " ", "Log out")
    option = input("Enter the number to book a flight or a option: ")
    try:
        optNum = int(option)
        if optNum<0 or optNum>len(rs)+3:
            print("Not valid number")
        elif optNum == len(rs)+1:
            printInfo(email, CONN_STRING, source, dest, dep_date, "2")
        elif optNum == len(rs)+2:
            flight = input("Enter the number before the flight you want to book: ")
            
        elif optNum == len(rs)+3:
            main.menu(email, CONN_STRING)
        elif optNum == len(rs)+4:
            return
        else:
            pass
            
    except:
        print("Not valid number")
    

def search(email, CONN_STRING):
    source = input("Source: ").upper()
    dest = input("Destination: ").upper()
    dep_date = input("Departure Date (DD/MM/YYYY): ")
    printInfo(email, CONN_STRING, source, dest, dep_date)
    


    
