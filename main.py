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
        menu()

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
        
def menu():
    print("===============================================")
    print("1. Search For Flights")
    print("2. List Existing Bookings")
    print("3. Logout")
    option = input()
    if option == "1":
        pass
    elif option == "2":
        pass
    elif option == "3":
        init()

def search():
    sorce = input("Source: ")
    dest = input("Destination: ")
    

if __name__ == "__main__":
    conToDB()
    init()
