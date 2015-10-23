import sys
import cx_Oracle
import getpass

CONN_STRING = ""

def conToDB():
    # get username
    user = input("Username [%s]: " % getpass.getuser())
    if not user:
        user = getpass.getuser()

    # get password
    pw = getpass.getpass()

    # the URL we are connecting to
    global CONN_STRING
    CONN_STRING = '' + user + '/' + pw + '@gwynne.cs.ualberta.ca:1521/CRS'
    

def sqlWithReturn(sql):
    con = cx_Oracle.connect(CONN_STRING)
    curs = con.cursor()
    curs.execute(sql)
    con.commit()
    rows = curs.fetchall()
    con.close()
    return rows

def sqlWithNoReturn(sql):
    con = cx_Oracle.connect(CONN_STRING)
    curs = con.cursor()
    curs.execute(sql)
    con.commit()
    con.close()

def init():
    print("===============================================")
    print("welcome to our system")
    print("1. Log in")
    print("2. Register")
    print("3. Exit")
    print("please enter the number in front of the option");
    option = input();
    if option == "1":
        logIn()
    elif option == "2":
        register()
    elif option == "3":
        pass
    else:
        print("Incorrect option, please enter correct number.")
        init()

def logIn():
    email = input("Email: ")
    pwd = getpass.getpass()
    sql = ("select * from users where email = '"
           + email + "' and pass = '" + pwd + "'")
    rs = sqlWithReturn(sql)
    if len(rs) == 0:
        print("Log in failed")
        init()
    else:
        sql = ("update users set last_login = sysdate where email = '"
               + email + "'")
        sqlWithNoReturn(sql)
        menu(email)

def register():
    try:
        email = input("Email: ")
        if len(email) == 0:
            print("email can not be empty")
            register()
        pwd = getpass.getpass()
        sql = ("insert into users values('" + email
               + "', '" + pwd + "', sysdate)")
        sqlWithNoReturn(sql)
        print("Successfully registed")
        menu()
    except:
        print("register failed: email already exists")
        init()
        
def menu(email):
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
    having fa.limit-count(tno) > 0;
    """
    try:
        sqlWithNoReturn(sql)
    except:
        pass
    sql = """
    create view good_connections (src,dst,dep_date,flightno1,
          flightno2, layover,price) 
    as
    select a1.src, a2.dst, a1.dep_date, a1.flightno, a2.flightno,
           a2.dep_time-a1.arr_time, min(a1.price+a2.price)
    from available_flights a1, available_flights a2
    where a1.dst=a2.src and a1.arr_time +1.5/24 <=a2.dep_time 
          and a1.arr_time +5/24 >=a2.dep_time
    group by a1.src, a2.dst, a1.dep_date, a1.flightno, a2.flightno, 
             a2.dep_time, a1.arr_time;
    """
    try:
        sqlWithNoReturn(sql)
    except:
        pass
    print("===============================================")
    print("1. Search For And Book Flights")
    print("2. List Or Cancel Existing Bookings")
    print("3. Logout")
    option = input()
    if option == "1":
        search()
    elif option == "2":
        pass
    elif option == "3":
        init()

def search():
    source = input("Source: ").upper()
    dest = input("Destination: ").upper()
    dep_date = input("Departure Date (yyyy-mm-dd): ")
    sql = ("select * from available_flights where upper(src) = '"
           + source + "' and upper(dst) = '" + dest
           + "' and dep_time = to_date('" + dep_date 
           + "', 'yyyy-dd-mm')")
    print(sql)
    rs = sqlWithReturn(sql)
    if len(rs) != 0:
        for row in rs:
            print(row)
    else:
        sql = """
        select * from available_flights af, airports a1, airports a2
        where a1.name like '%{0}%' or a1.city like '%{0}%'
              and a1.acode = af.src
              and a2.name like '%{1}%' or a2.city like '%{1}%'
              and a2.acode = af.dst
              and af.dep_time = to_date('{2}', 'yyyy-dd-mm')
        """.format(source, dest, dep_date)
        print(sql)
        rs = sqlWithReturn(sql)
        if len(rs) != 0:
            for row in rs:
                print(row)
        else:
            print("no results")

if __name__ == "__main__":
    conToDB()
    init()
