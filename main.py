import sys
import cx_Oracle
import getpass
import agents
import search

def conToDB():
    # get username
    user = input("Username [%s]: " % getpass.getuser())
    if not user:
        user = getpass.getuser()

    # get password
    pw = getpass.getpass()

    # the URL we are connecting to
    CONN_STRING = '' + user + '/' + pw + '@gwynne.cs.ualberta.ca:1521/CRS'
    init(CONN_STRING)
    
def sqlWithReturnDesc(sql, CONN_STRING):
    con = cx_Oracle.connect(CONN_STRING)
    curs = con.cursor()
    curs.execute(sql)
    con.commit()
    rows = curs.fetchall()
    desc = curs.description
    con.close()
    return rows, desc

def sqlWithReturn(sql, CONN_STRING):
    con = cx_Oracle.connect(CONN_STRING)
    curs = con.cursor()
    curs.execute(sql)
    con.commit()
    rows = curs.fetchall()
    con.close()
    return rows

def sqlWithNoReturn(sql, CONN_STRING):
    con = cx_Oracle.connect(CONN_STRING)
    curs = con.cursor()
    curs.execute(sql)
    con.commit()
    con.close()

def init(CONN_STRING):
    print("===============================================")
    print("welcome to our system")
    print("1. Log in")
    print("2. Register")
    print("3. Exit")
    print("please enter the number in front of the option");
    option = input();
    if option == "1":
        logIn(CONN_STRING)
    elif option == "2":
        register(CONN_STRING)
    elif option == "3":
        pass
    else:
        print("Incorrect option, please enter correct number.")
        init(CONN_STRING)

def logIn(CONN_STRING):
    email = input("Email: ")
    pwd = getpass.getpass()
    sql = ("select * from users where email = '"
           + email + "' and pass = '" + pwd + "'")
    try:
        rs = sqlWithReturn(sql, CONN_STRING)
    except:
        print("Log in failed")
        init(CONN_STRING)
    if len(rs) == 0:
        print("Log in failed")
        init(CONN_STRING)
    else:
        print("Log in success")
        menu(email, CONN_STRING)

def register(CONN_STRING):
    try:
        email = input("Email: ")
        if len(email) == 0:
            print("email can not be empty")
            register(CONN_STRING)
        pwd = getpass.getpass()
        while len(pwd) == 0:
            print("password can not be empty")
            pwd = getpass.getpass()
        sql = ("insert into users values('" + email
               + "', '" + pwd + "', sysdate)")
        sqlWithNoReturn(sql, CONN_STRING)
        print("Successfully registed")
        menu(email, CONN_STRING)
    except:
        print("register failed: email already exists")
        init(CONN_STRING)
        
def menu(email, CONN_STRING):
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
    print("===============================================")
    print("1. Search For And Book Flights")
    print("2. List Or Cancel Existing Bookings")
    print("3. Logout")
    sql = "select * from airline_agents where email = '{0}'".format(email)
    isAgent = sqlWithReturn(sql, CONN_STRING)
    if len(isAgent) > 0:
        print("4. Record a flight departure")
        print("5. Record a flight arrival")
    option = input()
    if len(isAgent) > 0 and option == "4":
        agents.recordDepart(email, CONN_STRING)
    if len(isAgent) > 0 and option == "5":
        agents.recordArr(email, CONN_STRING)
    if option == "1":
        search.search(email, CONN_STRING)
    elif option == "2":
        pass
    elif option == "3":
        sql = ("update users set last_login = sysdate where email = '"
               + email + "'")
        sqlWithNoReturn(sql, CONN_STRING)
        init(CONN_STRING)
    else:
        print("not a valid number")
        menu(email, CONN_STRING)

if __name__ == "__main__":
    conToDB()
