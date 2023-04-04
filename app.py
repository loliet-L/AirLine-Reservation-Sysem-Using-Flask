#  & "c:/STUDY/MINI-PROJECT/AIRLINE SYSTEM/env/Scripts/python.exe" "c:/STUDY/MINI-PROJECT/AIRLINE SYSTEM/app.py"
from os import error
import re
from flask import Flask , render_template , request
from flask_mysqldb import MySQLdb
import mysql.connector
from datetime import datetime

app = Flask(__name__)
mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database='airline_reservation_system'
    )

#  ---------------REGISTER PAGE----------- 
@app.route("/",methods=['POST','GET'])
def register(): 
    if(request.method=='POST'):
        name = str(request.form['name1']) 
        email = str(request.form['email'])
        username = str(request.form['S_uname'])
        upass = str(request.form['S_pass'])
        uCpass = str(request.form['Cpass'])
        
        # print("Before gender")

        gender = str(request.form['gender'])
        # print("after gender")
        phone = str(request.form['phone'])
        
        
        if ((upass == uCpass) and (len(phone) == 10) and upass.isdigit and upass.isupper and len(upass)<8):        
            cursor = mydb.cursor()
            cursor.execute("INSERT INTO user_info (user_name, name ,email , gender, password ,ph_no) VALUES (%s,%s,%s,%s,%s,%s)" , (username,name , email , gender , upass , phone))
            mydb.commit()
            register_msg = "User Registered Successfully"
            return render_template('register.html',register_msg = register_msg)
        
        else :
            register_msg_er = "ENTER CORRECT DETAILS"
            return render_template('register.html',register_msg_er = register_msg_er)
    
    return render_template('register.html')



#  ---------------LOGIN PAGE-----------   
@app.route("/login",methods=['POST','GET'])
def authentication():
    if(request.method=='POST'):
        username = str(request.form['uname'])
        upass = str(request.form['pass'])

        cursor = mydb.cursor()

        cursor.execute("SELECT * FROM user_info WHERE user_name = '"+username+"' and password = '"+upass+"'")
        account = cursor.fetchone()

        if account :
            return render_template('home.html')

        else :
            msg = "Incorrecr User Id / Password ."
            print(msg)
            return render_template('login.html',msg = msg)
            # return msg

    return render_template('login.html')  


# ----------------HOME PAGE--------------
@app.route("/home", methods = ['GET', 'POST'])
def home():

    if(request.method=='POST'):
        '''Add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')

        cursor1 = mydb.cursor();
        cursor1.execute("INSERT INTO contacts (name ,email , subject ,msg , date) VALUES (%s,%s,%s,%s,%s)" , (name, email, subject, message, datetime.now()))
        mydb.commit()   
        return render_template('home.html')
    return render_template('home.html')


# ----------------SEARCH FLIGHTS START--------------  
  
@app.route("/search-flights", methods = ['GET', 'POST'])
def search_flight():
    if(request.method=='POST'):
        src = request.form.get('from_city')
        dest = request.form.get('to_city')
        cursor=mydb.cursor()
        if (src != dest):
            query_string = "SELECT * FROM flights WHERE (source = %s AND destination = %s)"
            cursor.execute(query_string,(src,dest))
            content =cursor.fetchall()

            return render_template('search-flights.html',content=content)
        else:
            error_msg = "NO FLIGHTS AVAILABLE"
            return render_template('search-flights.html',error_msg=error_msg)
            
    return render_template('search-flights.html')

# ----------------SEARCH FLIGHTS END-------------- 


# ----------------BOOK TICKET START-------------- 
@app.route("/book-ticket", methods = ['GET', 'POST'])
def book_ticket():
    if(request.method=='POST'):
        cursor = mydb.cursor()
        input_ticket_id = request.form.get('bt_flight_id')

        query = "SELECT * FROM flights WHERE flight_Id = %s"
        cursor.execute(query,(input_ticket_id,))
        flight_details = cursor.fetchone()
        # av_seats = flight_details[10]
        
        if flight_details :
            f_id = flight_details[0]
            actual_price = str(flight_details[7])
            input_flight_price = str(request.form.get('bt_price'))
            ticket_no = str(flight_details[0]) + str(flight_details[8])
            book_msg = "YOUR TICKET NUMBER IS : " + str(ticket_no)
            p_name = (request.form.get('bt_pname'))
       
            if (input_flight_price == actual_price):
                av_seats = int(flight_details[8]) - 1
                cursor = mydb.cursor()
                cursor.execute("INSERT INTO ticket (ticket_number ,flight_id , name) VALUES (%s,%s,%s)" , (ticket_no, f_id, p_name))
                mydb.commit()

                cursor1 = mydb.cursor()
                update = "UPDATE flights set available_seats = %s  WHERE flight_Id = %s "
                cursor1.execute(update,(av_seats,f_id))
                mydb.commit()
                return render_template('book-ticket.html',book_msg = book_msg)

            else:
                book_msg = "Enter correct details"
                return render_template('book-ticket.html',book_msg = book_msg)

        else:
            f_id_msg = "ENTER CORRECT FLIGHT ID"
            return render_template('book-ticket.html',f_id_msg = f_id_msg)

    return render_template('book-ticket.html')

# ----------------BOOK TICKET END-------------- 




    
    

# ----------------CANCEL TICKET START-------------- 

@app.route("/cancel-ticket",methods=['POST','GET'])
def cancel_ticket():
    if(request.method=='POST'):
        fticket_number = request.form.get('ct_num')
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM ticket WHERE ticket_number = '"+fticket_number+"'")
        details = cursor.fetchone()
        
        # query_string = "SELECT  * from ticket where ticket_number = %s"
        # cursor.execute(query_string,(ticket_number,))
        # details = cursor.fetchone()
        if details :
            # pass_name = details[3]
            flight_id = details[2]
            ticket_num = details[1]
            # print(pass_name)
            # print(flight_id)
            # print(ticket_num)
            mycursor  = mydb.cursor()
            delete_query = " DELETE FROM ticket WHERE ticket_number =  %s" 
            # cursor1.execute = "DELETE FROM ticket WHERE ticket_number = '" +ticket_num+"' "
            mycursor.execute(delete_query,(ticket_num,))
            mydb.commit()
            # print(str(cursor1.rowcount()),"record(s) deleted")
            # cursor1.execute(delete_query,(ticket_num))
            cursor2 = mydb.cursor()
            # fl_id = details[2]
            update_seats_query = "UPDATE flights SET available_seats = available_seats + 1  WHERE flight_Id = %s"
            cursor2.execute(update_seats_query,(flight_id,))
            mydb.commit()
            cancel_ticket_msg = "TICKET NO: " + ticket_num +" CANCELLED SUCESSFULLY"
            return render_template('cancel-ticket.html', cancel_ticket_msg = cancel_ticket_msg)

        else:
            print("Wrong ticket number")
            cancel_ticket_er = "ENTER CORRECT TICKET NUMBER"
            return render_template('cancel-ticket.html', cancel_ticket_er = cancel_ticket_er)

        
        # return render_template('cancel-ticket.html')     
    return render_template('cancel-ticket.html') 

# ----------------CANCEL TICKET END--------------



@app.route("/view-ticket",methods=['GET', 'POST'])
def viewTicket():
    if(request.method=='POST'):
        
        ticket_num=request.form.get('vt_ticket_num')
        print(ticket_num)
        cursor3 = mydb.cursor()
        query="SELECT * FROM ticket WHERE ticket_number = %s "
        cursor3.execute(query,(ticket_num,))
        t_info = cursor3.fetchone()

        if t_info:
            fl_id = t_info[2]
            pass_name = t_info[3]
            print("Flight_id : ",fl_id)
            print("Passenger Name:",pass_name)
            cursor2=mydb.cursor()
            query2='SELECT * FROM flights WHERE flight_ID = %s'
            cursor2.execute(query2,(fl_id,))
            f_details=cursor2.fetchone()
            source  = f_details[2]
            dest  = f_details[3]
            dept  = f_details[4]
            print("Source:",source)
            print("dest:",dest)
            print("deptarture:",dept)
            print("Ticket NO",ticket_num)

            return render_template('view-ticket.html',ticket_num=ticket_num, fl_id = fl_id, pass_name = pass_name , source = source ,dest = dest,dept=dept )

        else :
            cancel_ticket_error = "Enter correct ticket number"
            return render_template('view-ticket.html', cancel_ticket_error = cancel_ticket_error)
            

    return render_template('view-ticket.html')

app.run(debug=True)  
#  & "c:/STUDY/MINI-PROJECT/AIRLINE SYSTEM/env/Scripts/python.exe" "c:/STUDY/MINI-PROJECT/AIRLINE SYSTEM/app.py"
