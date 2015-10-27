import main

# This function is accessible to airline agents and takes their input to assign
# an actual departure date to flightnos in sch_flights
def recordDepart(email, CONN_STRING):
    # get user input
    flightno = input("Please enter the flight number: ")
    
    # check if the user entered a value
    if len(flightno) == 0:
        print("Flight number cannot be blank")
        main.menu(email, CONN_STRING)
        
    # get more user input
    dep_date = input("Please enter the departure date(DD/MM/YYYY): ")

    if len(dep_date) == 0:
        print("Departure date must have a value.")
        main.menu(email, CONN_STRING)
    
    # check if the user's input flight exists
    sql ="""
    select * from sch_flights 
    where flightno = '{0}' 
    and to_char(dep_date, 'DD/MM/YYYY') = '{1}'
    """.format(flightno, dep_date)
    try:
        output = main.sqlWithReturn(sql, CONN_STRING)
    except:
        print("Improper input. Please try again")
        main.menu(email, CONN_STRING)
    if len(output) == 0:
        print("There is no flight with that flight number and departure date")
        main.menu(email, CONN_STRING)
    
    # get the value of the date and time of the actual departure time
    act_dep_time = input("Please enter the actual departure time(DD/MM/YYYY HH24:MI): ")
    
    # create command to update act_dep_time in sch_flights table
    sql = "update sch_flights set act_dep_time = to_date('{0}', 'DD/MM/YYYY HH24:MI') where flightno = '{1}' and to_char(dep_date, 'DD/MM/YYYY') = '{2}'".format(act_dep_time, flightno, dep_date)

    # see if the command works
    try:
        main.sqlWithNoReturn(sql, CONN_STRING)
    except:
        # if it does not, tell the user and return to the menu
        print("failed to record")
        main.menu(email, CONN_STRING)
    # if it does, tell the user and return to the menu
    print("successfully recorded")
    main.menu(email, CONN_STRING)
    
# This function is accessible to airline agents and takes their input to assign
# an actual arrival date and time to flightnos in sch_flights
def recordArr(email, CONN_STRING):
    # get the user's desired flightno
    flightno = input("Please enter the flight number: ")
    
    # check if the user actually entered anything
    if len(flightno) == 0:
        print("Flight number cannot be blank")
        main.menu(email, CONN_STRING)
        
    # get the user's flight's desired departure date
    dep_date = input("Please enter the departure date(DD/MM/YYYY): ")
    
    # check if the user actually entered anything
    if len(dep_date) == 0:
        print("Departure date must have a value.")
        main.menu(email, CONN_STRING)
           
    # check if the user's input flight exists
    sql ="""
    select * from sch_flights 
    where flightno = '{0}' 
    and to_char(dep_date, 'DD/MM/YYYY') = '{1}'
    """.format(flightno, dep_date)
    try:
        output = main.sqlWithReturn(sql, CONN_STRING)
    except:
        print("Improper input. Please try again")
        main.menu(email, CONN_STRING)
    if len(output) == 0:
        print("There is no flight with that flight number and departure date")
        main.menu(email, CONN_STRING)
        
    # get the departure date and time from the user
    act_arr_time = input("Please enter the actual arrival time(DD/MM/YYYY HH24:MI): ")
    
    # sql command that sets the actual arrival time of the flight
    sql = "update sch_flights set act_arr_time = to_date('{0}', 'DD/MM/YYYY HH24:MI') where flightno = '{1}' and to_char(dep_date, 'DD/MM/YYYY') = '{2}'".format(act_arr_time, flightno, dep_date)

    # see if the command can successfully execute
    try:
        main.sqlWithNoReturn(sql, CONN_STRING)
    except:
        # if it can't, tell the user and go to the menu
        print("failed to record")
        main.menu(email, CONN_STRING)
    # if it can, tell the user and go to the menu
    print("successfully recorded")
    main.menu(email, CONN_STRING)
