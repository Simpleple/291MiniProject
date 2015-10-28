import sys
import cx_Oracle
import getpass
import existing
import roundtrip
import agents
import search

# connect to the database
def conToDB():
    # get username
    user = input("Username [%s]: " % getpass.getuser())
    if not user:
        user = getpass.getuser()

    # get password
    pw = getpass.getpass()

    # the URL we are connecting to
    CONN_STRING = '' + user + '/' + pw + '@gwynne.cs.ualberta.ca:1521/CRS'

    # try to use the connection string to connect to database
    # if failed to connect, prompt error message and ask user
    # for correct username/password
    try:
        rs = sqlWithReturnDesc("select * from users", CONN_STRING)
    except:
        print("Wrong username/password")
        conToDB()

    # initialize the system
    init(CONN_STRING)

# execute an sql command and return the rows and description of the columns
def sqlWithReturnDesc(sql, CONN_STRING):
    con = cx_Oracle.connect(CONN_STRING)
    curs = con.cursor()
    curs.execute(sql)
    con.commit()
    rows = curs.fetchall()
    desc = curs.description
    con.close()
    return rows, desc

# execute an sql command and return the rows
def sqlWithReturn(sql, CONN_STRING):
    con = cx_Oracle.connect(CONN_STRING)
    curs = con.cursor()
    curs.execute(sql)
    con.commit()
    rows = curs.fetchall()
    con.close()
    return rows

# execute an sql command without returning anything
def sqlWithNoReturn(sql, CONN_STRING):
    con = cx_Oracle.connect(CONN_STRING)
    curs = con.cursor()
    curs.execute(sql)
    con.commit()
    con.close()

# initial menu. allow the user to log in with an existing
# account, register for a new account or exit the program
def init(CONN_STRING):
    # print the options
    print("===============================================")
    print("welcome to our system")
    print("1. Log in")
    print("2. Register")
    print("3. Exit")
    print("please enter the number in front of the option");

    # get user input and call corresponding function
    option = input();
    if option == "1":
        return logIn(CONN_STRING)
    elif option == "2":
        return register(CONN_STRING)
    elif option == "3":
        return
    # if not valid, print error message call init again
    else:
        print("Incorrect option, please enter correct number.")
        return init(CONN_STRING)

# the user can login with an existing profile in the database
def logIn(CONN_STRING):
    # get email and password
    email = input("Email: ")
    pwd = getpass.getpass()
    sql = ("select * from users where email = '"
           + email + "' and pass = '" + pwd + "'")
    
    # check validity of account by searching from
    # users table.
    try:
        rs = sqlWithReturn(sql, CONN_STRING)
    except:
        print("Log in failed")
        return init(CONN_STRING)

    # if not found, print error message and call init
    # again
    if len(rs) == 0:
        print("Log in failed")
        return init(CONN_STRING)
    else:
        print("Log in success")
        return menu(email, CONN_STRING)

# register a new email and password
def register(CONN_STRING):
    # register a new account. add account information
    # to user table
    try:
        email = input("Email: ")
        if len(email) == 0:
            print("email can not be empty")
            return register(CONN_STRING)
        pwd = getpass.getpass()
        while len(pwd) == 0:
            print("password can not be empty")
            pwd = getpass.getpass()
        sql = ("insert into users values('" + email
               + "', '" + pwd + "', sysdate)")
        sqlWithNoReturn(sql, CONN_STRING)
        print("Successfully registed")
        return menu(email, CONN_STRING)
    # if failed to register, print error message, call
    # init to restart
    except:
        print("register failed: email already exists")
        return init(CONN_STRING)
        
# logout and record the last login time
def logout(email, CONN_STRING):
    sql = ("update users set last_login = sysdate where email = '"
           + email + "'")
    sqlWithNoReturn(sql, CONN_STRING)
    return init(CONN_STRING)   

# main menu of the program. provides uesrs with options of
# searching for flights, making a booking, view existing
# bookings, cancel an existing booking and logout.
# for airline agents, add two more options of recording 
# actual departure time and actual arrival time       
def menu(email, CONN_STRING):
    # create view available_flights which shows flights information
    # with empty seats if view does not exist
    sql = """
    create view available_flights(flightno, dep_date, src,dst,
          dep_time,arr_time,fare,seats, price) 
    as 
    select f.flightno, sf.dep_date, f.src, f.dst, 
           f.dep_time+(trunc(sf.dep_date)-trunc(f.dep_time)), 
           f.dep_time+(trunc(sf.dep_date)-trunc(f.dep_time))+
           (f.est_dur/60+a2.tzone-a1.tzone)/24, fa.fare, 
           fa.limit-count(tno), fa.price 
    from flights f, flight_fares fa, sch_flights sf, bookings b,
         airports a1, airports a2 
    where f.flightno=sf.flightno and f.flightno=fa.flightno 
          and f.src=a1.acode and f.dst=a2.acode 
          and fa.flightno=b.flightno(+) and fa.fare=b.fare(+) 
          and sf.dep_date=b.dep_date(+) 
    group by f.flightno, sf.dep_date, f.src, f.dst, f.dep_time,
             f.est_dur,a2.tzone, a1.tzone, fa.fare, fa.limit, 
             fa.price 
    having fa.limit-count(tno) > 0
    """
    try:
        sqlWithNoReturn(sql, CONN_STRING)
    except:
        pass

    # create view good_connections gives good connection flights
    # information if view does not exist
    sql = """
    create view good_connections (src,dst,dep_time,arr_time,
          dep_date,flightno1,flightno2,stops,layover,price,
          seats1, seats2, fare1, fare2) 
    as
    select a1.src, a2.dst, a1.dep_time, a2.arr_time,
           a1.dep_date, a1.flightno, a2.flightno, 2 stops,
           a2.dep_time-a1.arr_time, min(a1.price+a2.price),
           a1.seats as seats1, a2.seats as seats2,
           a1.fare as fare1, a2.fare as fare2
    from available_flights a1, available_flights a2
    where a1.dst=a2.src and a1.arr_time +1.5/24 <=a2.dep_time 
          and a1.arr_time +5/24 >=a2.dep_time
    group by a1.src, a2.dst, a1.dep_date, a1.flightno, a2.flightno, 
             a2.dep_time, a1.arr_time, a1.dep_time, a2.arr_time,
             a1.seats, a2.seats, a1.fare, a2.fare
    """
    try:
        sqlWithNoReturn(sql, CONN_STRING)
    except:
        pass

    # print options
    print("===============================================")
    print("1. Search For And Book Flights")
    print("2. List Or Cancel Existing Bookings")
    print("3. Logout")
    print("4. Search For Round Trip Flights")    

    # check if the user is an airline agent
    sql = "select * from airline_agents where email = '{0}'".format(email)
    isAgent = sqlWithReturn(sql, CONN_STRING)

    # if user is an agent, provides two more options of
    # record a flight departure or arrival
    if len(isAgent) > 0:
        print("5. Record a flight departure")
        print("6. Record a flight arrival")

    # call method according to the user's option
    # print error message if not a valid input
    option = input()
    if len(isAgent) > 0 and option == "5":
        return agents.recordDepart(email, CONN_STRING)
    if len(isAgent) > 0 and option == "6":
        return agents.recordArr(email, CONN_STRING)
    if option == "1":
        return search.search(email, CONN_STRING)
    elif option == "2":
        return existing.existing(email, CONN_STRING)
    elif option == "3":
        return logout(email, CONN_STRING)
    elif option == "4":
        return roundtrip.roundTrip(email, CONN_STRING)
    else:
        print("not a valid number")
        return menu(email, CONN_STRING)

if __name__ == "__main__":
    conToDB()
