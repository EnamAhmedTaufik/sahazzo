from email import message
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
import mysql.connector as sql
resultO = ""
resultD = ""
resultV = ""
resultA = ""
pin_D = 1
pin_O = 1
pin_V = 1
pin_A = 1

def signUpForm (data): 
    for keys,values in data.items():
            if keys == 'first_name': first_name = values
            if keys == 'last_name': last_name = values
            if keys == 'email': email = values
            if keys == 'contact': contact = values
            if keys == 'nid': nid = values
            if keys == 'password': password = values
            if keys == 'confirm_password': confirm_password = values
    return (first_name, last_name, email, contact, nid, password, confirm_password)

def logInForm (data): 
    for keys,values in data.items():
            if keys == 'email': email = values
            if keys == 'password': password = values
    return (email, password)


def findDetails(email, password, cursor):
    query =  "SELECT * FROM PERSON WHERE EMAIL ='{}' and PASSWORD ='{}'".format(email, password)
    cursor.execute(query)
    result = list(cursor.fetchone())
    result = {'FIRST_NAME': result[0],'LAST_NAME': result[1],	'EMAIL': result[2],	'CONTACT': result[3],	'NID': result[4],	'PASSWORD': result[5],	'ID':  result[6]}
    return result



# Create your views here.
def home(request):
    return render (request, 'accounts/home.html')

def LoginDonator(request):
    global resultD
    if request.method == 'POST':
        database = sql.connect( user = 'root', password = '', host = 'localhost', database = 'sahazzo')
        cursor = database.cursor()
        data = request.POST
        email, password = logInForm(data)
        query =  "SELECT ID, PASSWORD FROM PERSON WHERE ID = (SELECT D_ID FROM DONATOR WHERE EMAIL= '{}')".format(email)
        cursor.execute(query)
        result = tuple(cursor.fetchall())
        if result==() or password !=  result[0][1]:
            return render(request,"accounts/error.html")
        else:
            result = findDetails(email, password, cursor)
            resultD = result
            return render (request, 'accounts/donator_profile.html', resultD)
    return render (request, 'accounts/LoginDonator.html')

def LoginOrganizor(request):
    global resultO
    if request.method == 'POST':
        database = sql.connect( user = 'root', password = '', host = 'localhost', database = 'sahazzo')
        cursor = database.cursor()
        data = request.POST
        email, password = logInForm(data)
        query =  "SELECT ID, PASSWORD FROM PERSON WHERE ID = (SELECT O_ID FROM ORGANIZOR WHERE EMAIL= '{}')".format(email)
        cursor.execute(query)
        result = tuple(cursor.fetchall())
        if result==() or password !=  result[0][1]:
            return render(request,"accounts/error.html")
        else:
            result = findDetails(email, password, cursor)
            resultO = result
            return render (request, 'accounts/organizor_profile.html', resultO)
    return render (request, 'accounts/LoginOrganizor.html')

def LoginVolunteer(request):
    global resultV
    if request.method == 'POST':
        database = sql.connect( user = 'root', password = '', host = 'localhost', database = 'sahazzo')
        cursor = database.cursor()
        data = request.POST
        email, password = logInForm(data)
        query =  "SELECT ID, PASSWORD FROM PERSON WHERE ID = (SELECT V_ID FROM VOLUNTEER WHERE EMAIL= '{}')".format(email)
        cursor.execute(query)
        result = tuple(cursor.fetchall())
        if result==() or password !=  result[0][1]:
            return render(request,"accounts/error.html")
        else:
            result = findDetails(email, password, cursor)
            resultV = result
            query =  "SELECT STATUS FROM VOLUNTEER WHERE V_ID ='{}'".format(resultV['ID'])
            cursor.execute(query)
            result = tuple(cursor.fetchall())
            resultV ['STATUS'] = result[0][0]
            database.commit()
            return render (request, 'accounts/volunteer_profile.html', resultV)
    return render (request, 'accounts/LoginVolunteer.html')

def LoginAdmin (request):
    global resultA
    if request.method == 'POST':
        database = sql.connect( user = 'root', password = '', host = 'localhost', database = 'sahazzo')
        cursor = database.cursor()
        data = request.POST
        email, password = logInForm(data)
        query =  "SELECT * FROM PERSON WHERE EMAIL ='{}' and PASSWORD ='{}' and ID = 'A'".format(email, password)
        cursor.execute(query)
        result = tuple(cursor.fetchall())
        if result==():
            return render(request,"accounts/error.html")
        else:
            result = findDetails(email, password, cursor)
            resultA = result
            return render (request, 'accounts/admin_profile.html', resultA)
    return render (request, 'accounts/LoginAdmin.html')

def SignupDonator(request):
    global pin_D
    if request.method == 'POST':
        database = sql.connect( user = 'root', password = '', host = 'localhost', database = 'sahazzo')
        cursor = database.cursor()
        data = request.POST
        first_name, last_name, email, contact, nid, password, confirm_password = signUpForm(data)
        query =  "SELECT * FROM DONATOR WHERE EMAIL ='{}'".format(email)
        cursor.execute(query)
        result = tuple(cursor.fetchall())
        if result==():
            p_id = "D"+str(pin_D).zfill(5)
            query =  "INSERT INTO PERSON VALUES ('{}','{}','{}','{}','{}','{}','{}')".format(first_name, last_name, email, contact, nid, password,p_id)
            query2 =  "INSERT INTO DONATOR VALUES ('{}','{}')".format(p_id, email)
            cursor.execute(query)
            cursor.execute(query2)
            database.commit()
            pin_D += 1
        else:
            return render(request,"accounts/error.html") 
        messages.success(request, 'Success')       
        return render (request, 'accounts/home.html')
    return render (request, 'accounts/SignupDonator.html')

def SignupOrganizor(request):
    global pin_O
    if request.method == 'POST':
        database = sql.connect( user = 'root', password = '', host = 'localhost', database = 'sahazzo')
        cursor = database.cursor()  
        data = request.POST
        first_name, last_name, email, contact, nid, password, confirm_password = signUpForm(data)
        query =  "SELECT * FROM ORGANIZOR WHERE EMAIL ='{}'".format(email)
        cursor.execute(query)
        result = tuple(cursor.fetchall())
        if result==():
            p_id = "O"+str(pin_O).zfill(5)
            query =  "INSERT INTO PERSON VALUES ('{}','{}','{}','{}','{}','{}','{}')".format(first_name, last_name, email, contact, nid, password,p_id)
            query2 =  "INSERT INTO ORGANIZOR VALUES ('{}','{}')".format(p_id, email)
            cursor.execute(query)
            cursor.execute(query2)
            database.commit()
            pin_O += 1
        else:
            return render(request,"accounts/error.html")
        messages.success(request, 'Success')
        return render (request, 'accounts/home.html')
    return render (request, 'accounts/SignupOrganizor.html')

def SignupVolunteer(request):
    global pin_V
    if request.method == 'POST':
        database = sql.connect( user = 'root', password = '', host = 'localhost', database = 'sahazzo')
        cursor = database.cursor()
        data = request.POST
        first_name, last_name, email, contact, nid, password, confirm_password = signUpForm(data)
        query =  "SELECT * FROM VOLUNTEER WHERE EMAIL ='{}'".format(email)
        cursor.execute(query)
        result = tuple(cursor.fetchall())
        if result==():
            p_id = "V"+str(pin_V).zfill(5)
            query =  "INSERT INTO PERSON VALUES ('{}','{}','{}','{}','{}','{}','{}')".format(first_name, last_name, email, contact, nid, password,p_id)
            query2 =  "INSERT INTO VOLUNTEER VALUES ('{}','{}','{}','{}')".format(p_id, email, 'Not in volunteering work', 'Null')
            cursor.execute(query)
            cursor.execute(query2)
            database.commit()
            pin_V += 1
        else:
            return render(request,"accounts/error.html")
        messages.success(request, 'Success')
        return render (request, 'accounts/home.html')
    return render (request, 'accounts/SignupVolunteer.html')

def donator_profile(request):
    global resultD
    return render (request, 'accounts/donator_profile.html', resultD)
def organizor_profile(request):
    global resultO
    return render (request, 'accounts/organizor_profile.html', resultO)
def volunteer_profile(request):
    global resultV
    v_id = resultV['ID']
    database = sql.connect( user = 'root', password = '', host = 'localhost', database = 'sahazzo')
    cursor = database.cursor()
    query =  "SELECT STATUS FROM VOLUNTEER WHERE V_ID ='{}'".format(v_id)
    cursor.execute(query)
    result = tuple(cursor.fetchall())
    resultV ['STATUS'] = result[0][0]
    database.commit()
    return render (request, 'accounts/volunteer_profile.html', resultV)

def admin_profile(request):
    global resultA
    return render (request, 'accounts/admin_profile.html', resultA)

event_counter, Event_Name, Start_Time, End_Time, Location, Budget, Shop, Items, Quantity, Event_For= 1, '', '','','','','','','',''
def create_event(request):
    global event_counter, Event_Name, Start_Time, End_Time, Location, Budget, Shop, Items, Quantity, Event_For, resultO
    mail = resultO['EMAIL']
    if request.method == 'POST':
        e_id = "E" + str(event_counter).zfill(4)
        event_counter += 1
        database = sql.connect( user = 'root', password = '', host = 'localhost', database = 'sahazzo')
        cursor = database.cursor()  
        data = request.POST
        for keys,values in data.items():
            if keys == 'Event_Name': Event_Name = values
            if keys == 'Start_Time': Start_Time = values
            if keys == 'End_Time': End_Time = values
            if keys == 'Location': Location = values
            if keys == 'Budget': Budget = values
            if keys == 'Shop': Shop = values
            if keys == 'Items': Items = values
            if keys == 'Quantity': Quantity = values
            if keys == 'Event_For': Event_For = values
        query =  "SELECT * FROM EVENT WHERE Event_Name ='{}' and Location ='{}' and Items ='{}' and Event_For ='{}'".format(Event_Name,Location,Items,Event_For)
        cursor.execute(query)
        result = tuple(cursor.fetchall())
        if result==():
            query =  "INSERT INTO EVENT VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(Event_Name, Start_Time, End_Time, Location, Budget, Shop, Items, Quantity, Event_For,e_id, mail)
            query2 =  "INSERT INTO FUND VALUES ('{}','{}','{}','{}')".format(e_id, 0, 'Not Fulfilled', 'Not Taken')
            query3 =  "INSERT INTO SHOP VALUES ('{}','{}','{}','{}')".format(Shop, e_id, Budget, 'Pending')
            cursor.execute(query)
            cursor.execute(query2)
            cursor.execute(query3)
            database.commit()
        else:
            return render(request,"accounts/error.html")
        messages.success(request, 'Success')
    return render (request, 'accounts/create_event.html')


def event_details_o(request):
    global resultO
    mail = resultO['EMAIL']
    database = sql.connect( user = 'root', password = '', host = 'localhost', database = 'sahazzo')
    cursor = database.cursor()
    query =  "SELECT * FROM EVENT WHERE Created_by  ='{}'".format(mail)
    cursor.execute(query)
    result = tuple(cursor.fetchall())
    if result==():
        return render(request,"accounts/error.html")
    else:
        database.commit()
        a_dict = {}
        for i in result:
            a_dict[i[9]] = [i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9]]
    return render (request, 'accounts/event_details_o.html', {'a_dict': a_dict})

def packages(request):
    return render (request, 'accounts/packages.html')

def event_details_d(request):
    global resultD
    database = sql.connect( user = 'root', password = '', host = 'localhost', database = 'sahazzo')
    cursor = database.cursor()
    query =  "SELECT * FROM EVENT"
    cursor.execute(query)
    result = tuple(cursor.fetchall())
    query2 =  "SELECT * FROM FUND"
    cursor.execute(query2)
    result2 = tuple(cursor.fetchall())
    a_dict = {}
    for i in result:
        for  j in result2:
            if j[1] < i[4] and j[0] == i[9]: 
                a_dict[j[0]] = [i[0],i[4],j[0],int(i[4])-int(j[1]),i[3]]

    if request.method == 'POST':
        data = request.POST
        for keys,values in data.items():
            if keys == 'id': id = values
            if keys == 'amount': amount = values
        query3 =  "SELECT EVENT_ID, COLLECTED_AMOUNT, Fund_Status FROM FUND WHERE EVENT_ID= '{}'".format(id)
        cursor.execute(query3)
        result3 = tuple(cursor.fetchall())
        query4 =  "SELECT Budget FROM EVENT WHERE EVENT_ID= '{}'".format(id)
        cursor.execute(query4)
        result4 = tuple(cursor.fetchall())
        if int(amount) > int(result4[0][0])- int(result3[0][1]):
            return render(request,"accounts/error.html")
        else:
            total_amount = int(amount) + int(result3[0][1])
        if total_amount == int(result4[0][0]):
            status = "Fulfilled"
        else:
            status = "Not Fulfil"
        query5 =  "Update FUND set COLLECTED_AMOUNT = '{}', Fund_Status = '{}' WHERE EVENT_ID= '{}'".format(total_amount,status,id)
        cursor.execute(query5)
        query6 =  "INSERT INTO DONATE VALUES ('{}','{}','{}','{}')".format(resultD['ID'], id, 'Bkash', amount)
        cursor.execute(query6)
        database.commit()
        messages.success(request, 'Success')
        return render (request, 'accounts/donator_profile.html', resultD)
    else:
        return render (request, 'accounts/event_details_d.html', {'a_dict': a_dict})

def donateHistory(request):
    global resultD
    d_id = resultD['ID']
    database = sql.connect( user = 'root', password = '', host = 'localhost', database = 'sahazzo')
    cursor = database.cursor()
    query =  "SELECT * FROM DONATE WHERE D_ID ='{}'".format(d_id)
    cursor.execute(query)
    result = tuple(cursor.fetchall())
    if result==():
        return render(request,"accounts/error.html")
    else:
        database.commit()
        a_dict = {}
        key = 1
        for i in result:
            a_dict[str(key)] = [i[1],i[2],i[3]]
            key += 1
    return render (request, 'accounts/donateHistory.html', {'a_dict': a_dict})

def event_details_v(request):
    global resultV
    v_id = resultV['ID']
    database = sql.connect( user = 'root', password = '', host = 'localhost', database = 'sahazzo')
    cursor = database.cursor()
    query =  "SELECT * FROM EVENT"
    cursor.execute(query)
    result = tuple(cursor.fetchall())
    database.commit()
    a_dict = {}
    for i in result:
        a_dict[i[9]] = [i[0],i[2],i[3],i[9]]

    if request.method == 'POST':
        data = request.POST
        for keys,values in data.items():
            if keys == 'id': id = values

        query2 =  "SELECT STATUS, VOLUNTARY FROM VOLUNTEER WHERE V_ID= '{}'".format(v_id)
        cursor.execute(query2)
        result2 = tuple(cursor.fetchall())
        if 'Not in volunteering' in result2[0][0]:     
            query3 =  "Update VOLUNTEER set STATUS = '{}', VOLUNTARY = '{}' WHERE V_ID= '{}'".format('In volunteering',id,v_id)
            cursor.execute(query3)
            database.commit()
        else:
            return render(request,"accounts/error.html")
        resultV ['STATUS'] = 'In volunteering'
        return render (request, 'accounts/volunteer_profile.html', resultV)
    else:
        return render (request, 'accounts/event_details_v.html', {'a_dict': a_dict})

def voluntaryHistory(request):
    global resultv
    v_id = resultV['ID']
    database = sql.connect( user = 'root', password = '', host = 'localhost', database = 'sahazzo')
    cursor = database.cursor()
    query =  "SELECT * FROM VOLUNTEER WHERE V_ID ='{}'".format(v_id)
    cursor.execute(query)
    result = tuple(cursor.fetchall())
    if result==():
        return render(request,"accounts/error.html")
    else:
        database.commit()
        a_dict = {}
        for i in result:
            a_dict[v_id] = [i[3]]
    return render (request, 'accounts/voluntaryHistory.html', {'a_dict': a_dict})

def manageEvents(request):
    database = sql.connect( user = 'root', password = '', host = 'localhost', database = 'sahazzo')
    cursor = database.cursor()
    query =  "Select event.event_id, event_name, location, budget, created_by, collected_amount, shop from event inner join fund on event.event_id = fund.event_id"
    cursor.execute(query)
    result = tuple(cursor.fetchall())
    query =  "select count(event_name) from event"
    cursor.execute(query)
    info1 = (cursor.fetchone())
    query =  "select count(event_name) from event where event_for ='Myself'"
    cursor.execute(query)
    info2 = (cursor.fetchone())
    query =  "select count(event_name) from event where event_for ='My family'"
    cursor.execute(query)
    info3 = (cursor.fetchone())
    query =  "select count(event_name) from event where event_for ='People of my area'"
    cursor.execute(query)
    info4 = (cursor.fetchone())
    database.commit()
    a_dict, b_dict = {}, {}
    for i in result:
        a_dict[i[0]] = [i[0],i[1],i[2],i[3],i[4],i[5],i[6]]
    b_dict['INFO'] = [info1[0],info2[0],info3[0],info4[0]]
    return render (request, 'accounts/manageEvents.html', {'a_dict': a_dict, 'b_dict': b_dict})

def shopPayment(request):
    database = sql.connect( user = 'root', password = '', host = 'localhost', database = 'sahazzo')
    cursor = database.cursor()
    query =  "Select shop_name, event.event_name, pay_demand, delivery_status, event.event_id from event inner join shop on event.event_id = shop.event_id"
    cursor.execute(query)
    result = (cursor.fetchall())
    query =  "select count(distinct(Shop_Name)) from shop"
    cursor.execute(query)
    info1 = (cursor.fetchone())
    query =  "select sum(PAY_DEMAND) from shop where DELIVERY_STATUS = 'Processing'"
    cursor.execute(query)
    info2 = (cursor.fetchone())
    query =  "select sum(PAY_DEMAND) from shop where DELIVERY_STATUS = 'Pending'"
    cursor.execute(query)
    info3 = (cursor.fetchone())
    database.commit()
    a_dict, b_dict = {}, {}
    for i in result:
        a_dict[i[4]] = [i[0],i[1],i[2],i[3],i[4]]
    b_dict['INFO'] = [info1[0],info2[0],info3[0]]
    print(b_dict)
    return render (request, 'accounts/shopPayment.html', {'a_dict': a_dict, 'b_dict': b_dict})

def collectFund(request):
    database = sql.connect( user = 'root', password = '', host = 'localhost', database = 'sahazzo')
    cursor = database.cursor()
    query =  "Select event.event_id, event_name, budget, collected_amount, fund_taken_by from event inner join fund on event.event_id = fund.event_id"
    cursor.execute(query)
    result = tuple(cursor.fetchall())
    query =  "select count(*) from fund"
    cursor.execute(query)
    info1 = tuple(cursor.fetchall())
    query =  "Select count(*) from fund where Fund_Status = 'Not Fulfil'"
    cursor.execute(query)
    info2 = tuple(cursor.fetchall())
    query =  "select sum(COLLECTED_AMOUNT) from fund"
    cursor.execute(query)
    info3 = tuple(cursor.fetchall())
    query =  "Select count(*) from fund where Fund_Status = 'Fulfilled'"
    cursor.execute(query)
    info4 = tuple(cursor.fetchall())
    database.commit()
    a_dict,b_dict = {}, {}
    for i in result:
        a_dict[i[0]] = [i[0],i[1],i[2],i[3],i[4]]
    b_dict['INFO'] = [info1[0][0],info3[0][0],info2[0][0],info4[0][0]]
    return render (request, 'accounts/collectFund.html',  {'a_dict': a_dict,'b_dict': b_dict})

def donatorDatabase(request):
    database = sql.connect( user = 'root', password = '', host = 'localhost', database = 'sahazzo')
    cursor = database.cursor()
    query =  "Select FIRST_NAME, LAST_NAME, Person.EMAIL, CONTACT, NID, PASSWORD, ID from PERSON inner join Donator on Person.ID = Donator.D_ID"
    cursor.execute(query)
    result = (cursor.fetchall())
    query =  "select count(EMAIL) from donator"
    cursor.execute(query)
    info1 = (cursor.fetchone())
    query =  "select count(distinct(D_ID)) from donate"
    cursor.execute(query)
    info2 = (cursor.fetchone())
    info3 = str(int(info1[0])-int(info2[0]))
    query =  "select sum(PAYMENT) from donate"
    cursor.execute(query)
    info4 = (cursor.fetchone())
    database.commit()
    d_database, b_dict = {}, {}
    for i in result:
        d_database[i[6]] = [i[6],i[0]+' '+i[1],i[2],i[3],i[4]]
    b_dict['INFO'] = [info1[0],info2[0],info3[0],info4[0]]
    return render (request, 'accounts/donatorDatabase.html', {'d_database': d_database, 'b_dict': b_dict})

def volunteerDatabase(request):
    database = sql.connect( user = 'root', password = '', host = 'localhost', database = 'sahazzo')
    cursor = database.cursor()
    query =  "Select FIRST_NAME, LAST_NAME, Person.EMAIL, CONTACT, NID, PASSWORD, ID, VOLUNTEER.STATUS, VOLUNTEER.VOLUNTARY from PERSON inner join VOLUNTEER on Person.ID = VOLUNTEER.V_ID"
    cursor.execute(query)
    result = tuple(cursor.fetchall())
    query =  "select count(EMAIL) from volunteer"
    cursor.execute(query)
    info1 = (cursor.fetchone())
    query =  "select count(STATUS) from volunteer where STATUS = 'In volunteering'"
    cursor.execute(query)
    info2 = (cursor.fetchone())
    query =  "select count(STATUS) from volunteer where STATUS = 'Not in volunteering'"
    cursor.execute(query)
    info3 = (cursor.fetchone())
    database.commit()
    v_database, b_dict = {}, {}
    for i in result:
        v_database[i[6]] = [i[6],i[0]+' '+i[1],i[2],i[3],i[4],i[7],i[8]]
    b_dict['INFO'] = [info1[0],info2[0],info3[0]]
    return render (request, 'accounts/volunteerDatabase.html', {'v_database': v_database, 'b_dict': b_dict})

def organizorDatabase(request):
    database = sql.connect( user = 'root', password = '', host = 'localhost', database = 'sahazzo')
    cursor = database.cursor()
    query =  "Select FIRST_NAME, LAST_NAME, Person.EMAIL, CONTACT, NID, PASSWORD, ID from PERSON inner join Organizor on Person.ID = Organizor.O_ID"
    cursor.execute(query)
    result = tuple(cursor.fetchall())
    query =  "select count(EMAIL) from organizor"
    cursor.execute(query)
    info1 = (cursor.fetchone())
    query =  "select count(distinct(created_by)) from event"
    cursor.execute(query)
    info2 = (cursor.fetchone())
    info3 = str(int(info1[0])-int(info2[0]))
    database.commit()
    o_database, b_dict = {}, {}
    for i in result:
        o_database[i[6]] = [i[6],i[0]+' '+i[1],i[2],i[3],i[4]]
    b_dict['INFO'] = [info1[0],info2[0],info3[0]]
    return render (request, 'accounts/organizorDatabase.html', {'o_database': o_database, 'b_dict': b_dict})


def updatePerson(request, id):
    global resultA
    database = sql.connect( user = 'root', password = '', host = 'localhost', database = 'sahazzo')
    cursor = database.cursor()
    query =  "SELECT * FROM PERSON WHERE ID ='{}'".format(id)
    cursor.execute(query)
    result = list(cursor.fetchone())
    a_dict = {'FIRST_NAME': result[0],'LAST_NAME': result[1],'EMAIL': result[2],'CONTACT': result[3],'NID': result[4],'PASSWORD': result[5],'ID':result[6]}
    if 'V' in id:
        query2 =  "SELECT * FROM VOLUNTEER WHERE V_ID ='{}'".format(id)
        cursor.execute(query2)
        result2 = list(cursor.fetchone())
        a_dict = {'FIRST_NAME': result[0],'LAST_NAME': result[1],'EMAIL': result[2],'CONTACT': result[3],'NID': result[4],'PASSWORD': result[5],'ID':result[6], 'STATUS': result2[2], 'VOLUNTARY':result2[3]}
        b_list=[]
        query =  "select event_id from event"
        cursor.execute(query)
        result = list(cursor.fetchall())
        for i in result:
            b_list.append(i)
        a_dict['all_event_id'] = b_list
    if request.method == 'POST':
        data = request.POST
        for keys,values in data.items():
            if keys == 'FIRST_NAME': FIRST_NAME = values
            if keys == 'LAST_NAME': LAST_NAME = values
            if keys == 'EMAIL': EMAIL = values
            if keys == 'CONTACT': CONTACT = values
            if keys == 'NID': NID = values
            if keys == 'STATUS': STATUS = values
            if keys == 'VOLUNTARY': VOLUNTARY = values
        query4 =  "UPDATE PERSON SET FIRST_NAME = '{}', LAST_NAME = '{}', EMAIL = '{}', CONTACT = '{}', NID = '{}' WHERE ID = '{}'".format(FIRST_NAME, LAST_NAME, EMAIL, CONTACT, NID, id)
        if 'V' in id:
            if STATUS == 'In volunteering' and VOLUNTARY == 'Null':
                return render(request,"accounts/error.html")
            elif VOLUNTARY != 'Null':
                STATUS = 'In volunteering'
            elif STATUS == 'Not in volunteering':
                VOLUNTARY = 'Null'
            query3 =  "UPDATE VOLUNTEER SET STATUS = '{}', VOLUNTARY = '{}' WHERE V_ID = '{}'".format(STATUS, VOLUNTARY, id)
            cursor.execute(query3)
        cursor.execute(query4)
        database.commit()
        messages.success(request, 'Success')
        return render (request, 'accounts/admin_profile.html', resultA)
    database.commit()
    return render (request, 'accounts/updatePerson.html', a_dict)
    

def deletePerson(request, id):
    global resultA
    database = sql.connect( user = 'root', password = '', host = 'localhost', database = 'sahazzo')
    cursor = database.cursor()
    query =  "SELECT * FROM PERSON WHERE ID ='{}'".format(id)
    cursor.execute(query)
    result = list(cursor.fetchone())
    a_dict = {'FIRST_NAME': result[0],'LAST_NAME': result[1],'EMAIL': result[2],'CONTACT': result[3],'NID': result[4],'PASSWORD': result[5],'ID':result[6]}
    if 'V' in id:
        query2 =  "SELECT * FROM VOLUNTEER WHERE V_ID ='{}'".format(id)
        cursor.execute(query2)
        result2 = list(cursor.fetchone())
        a_dict = {'FIRST_NAME': result[0],'LAST_NAME': result[1],'EMAIL': result[2],'CONTACT': result[3],'NID': result[4],'PASSWORD': result[5],'ID':result[6], 'STATUS': result2[2], 'VOLUNTARY':result2[3]}
    if request.method == 'POST':
        messages.success(request, 'success')
        if 'D' in id:
            query3 =  "DELETE FROM DONATOR WHERE D_ID = '{}'".format(id)
            query4 =  "DELETE FROM PERSON WHERE ID = '{}' and EMAIL = '{}'".format(id, result[2])
            cursor.execute(query3)
            cursor.execute(query4)
            database.commit()
        if 'O' in id:
            query3 =  "DELETE FROM ORGANIZOR WHERE O_ID = '{}'".format(id)
            query4 =  "DELETE FROM PERSON WHERE ID = '{}' and EMAIL = '{}'".format(id, result[2])
            cursor.execute(query3)
            cursor.execute(query4)
            database.commit()
        if 'V' in id:
            query3 =  "DELETE FROM VOLUNTEER WHERE V_ID = '{}'".format(id)
            query4 =  "DELETE FROM PERSON WHERE ID = '{}' and EMAIL = '{}'".format(id, result[2])
            cursor.execute(query3)
            cursor.execute(query4)
            database.commit()
        return render (request, 'accounts/admin_profile.html', resultA)
    database.commit()
    return render (request, 'accounts/deletePerson.html', a_dict)


def updateEvent(request, id):
    global resultA
    database = sql.connect( user = 'root', password = '', host = 'localhost', database = 'sahazzo')
    cursor = database.cursor()
    query =  "Select event_id, event_name, location, budget, created_by, shop from event where event_id = '{}'".format(id)
    cursor.execute(query)
    result = list(cursor.fetchone())
    query2 =  "Select collected_amount, fund_taken_by from fund where event_id = '{}'".format(id)
    cursor.execute(query2)
    result2 = list(cursor.fetchone())
    database.commit()
    a_dict = {'EVENT_ID': result[0],'EVENT_NAME': result[1],'LOCATION': result[2],'BUDGET': result[3],'CREATED_BY': result[4],'COLLECTED_AMOUNT': result2[0],'SHOP':result[5]}
    if request.method == 'POST':
        data = request.POST
        for keys,values in data.items():
            if keys == 'EVENT_NAME': EVENT_NAME = values
            if keys == 'LOCATION': LOCATION = values
            if keys == 'BUDGET': BUDGET = values
            if keys == 'CREATED_BY': CREATED_BY = values
            if keys == 'COLLECTED_AMOUNT': COLLECTED_AMOUNT = values
            if keys == 'SHOP': SHOP = values
        query4 =  "UPDATE EVENT SET EVENT_NAME = '{}',  LOCATION = '{}', BUDGET = '{}', CREATED_BY = '{}' , SHOP = '{}' WHERE EVENT_ID = '{}'".format(EVENT_NAME,  LOCATION, BUDGET, CREATED_BY, SHOP, id)
        cursor.execute(query4)
        database.commit()
        messages.success(request, 'Success')
        return render (request, 'accounts/admin_profile.html', resultA)
    return render (request, 'accounts/updateEvent.html', a_dict)


def deleteEvent(request, id):
    global resultA
    database = sql.connect( user = 'root', password = '', host = 'localhost', database = 'sahazzo')
    cursor = database.cursor()
    query =  "Select event_id, event_name, location, budget, created_by, shop from event where event_id = '{}'".format(id)
    cursor.execute(query)
    result = list(cursor.fetchone())
    query2 =  "Select collected_amount from fund where event_id = '{}'".format(id)
    cursor.execute(query2)
    result2 = list(cursor.fetchone())
    database.commit()
    a_dict = {'EVENT_ID': result[0],'EVENT_NAME': result[1],'LOCATION': result[2],'BUDGET': result[3],'CREATED_BY': result[4],'COLLECTED_AMOUNT': result2[0],'SHOP':result[5]}
    if request.method == 'POST':
        query3 =  "DELETE FROM EVENT WHERE EVENT_ID = '{}'".format(id)
        cursor.execute(query3)
        database.commit()
        messages.success(request, 'Success')
        return render (request, 'accounts/admin_profile.html', resultA)
    return render (request, 'accounts/deleteEvent.html', a_dict)



def paymentConfirm(request, id):
    global resultA
    database = sql.connect( user = 'root', password = '', host = 'localhost', database = 'sahazzo')
    cursor = database.cursor()
    query =  "Select Shop_name, event_id, pay_demand from shop where event_id = '{}'".format(id)
    cursor.execute(query)
    result = list(cursor.fetchone())
    query2 =  "Select event_name from event where event_id = '{}'".format(id)
    cursor.execute(query2)
    result2 = list(cursor.fetchone())
    database.commit()
    a_dict = {'SHOP_NAME': result[0],'EVENT_NAME': result2[0],'EVENT_ID': result[1],'PAY_DEMAND': result[2]}
    query3 =  "SELECT Fund_Status FROM FUND WHERE EVENT_ID= '{}'".format(id)
    cursor.execute(query3)
    result3 = (cursor.fetchone())
    if request.method == 'POST':
        if "Fulfilled" in result3:
            query4 =  "UPDATE SHOP SET DELIVERY_STATUS = 'Processing' WHERE EVENT_ID = '{}'".format(id)
            cursor.execute(query4)
            database.commit()
            messages.success(request, 'Success')
            return render (request, 'accounts/admin_profile.html', resultA)
        else:
            return render(request,"accounts/error.html")
    return render (request, 'accounts/paymentConfirm.html', a_dict)

    
def collectFundConfirm(request, id):
    global resultA
    database = sql.connect( user = 'root', password = '', host = 'localhost', database = 'sahazzo')
    cursor = database.cursor()
    query =  "Select EVENT_ID, COLLECTED_AMOUNT from fund where event_id = '{}'".format(id)
    cursor.execute(query)
    result = list(cursor.fetchone())
    query2 =  "Select EVENT_NAME, BUDGET from event where event_id = '{}'".format(id)
    cursor.execute(query2)
    result2 = list(cursor.fetchone())
    database.commit()
    a_dict = {'EVENT_ID': result[0],'EVENT_NAME': result2[0],'BUDGET': result2[1],'COLLECTED_AMOUNT': result[1]}
    if request.method == 'POST':
        if result2[1] ==  result[1]:
            query4 =  "UPDATE FUND SET FUND_TAKEN_BY = 'Taken By Admin' WHERE EVENT_ID = '{}'".format(id)
            cursor.execute(query4)
            database.commit()
            messages.success(request, 'Success')
            return render (request, 'accounts/admin_profile.html', resultA)
        else:
            return render(request,"accounts/error.html")
    return render (request, 'accounts/collectFundConfirm.html', a_dict)