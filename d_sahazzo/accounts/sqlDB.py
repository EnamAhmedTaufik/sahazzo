import mysql.connector
con = mysql.connector.connect(user = 'root', password = '', host = 'localhost', database = 'sahazzo')
cur = con.cursor()

#queryForModify= 'Alter table DONATOR modify column ID char(7)'

queryDropDatabase = 'Drop database sahazzo'

queryCreateDatabase = 'Create database sahazzo'

#queryDrop = 'Drop table VOLUNTEER'

queryCreatePersonTable = """CREATE TABLE PERSON (FIRST_NAME varchar(30) NOT NULL, LAST_NAME varchar(30) NOT NULL, EMAIL varchar(50) NOT NULL, CONTACT char(20) NOT NULL, NID char(20) NOT NULL, PASSWORD varchar(50) NOT NULL, ID char(7) NOT NULL, PRIMARY KEY(ID, EMAIL))"""

queryCreateDonatorTable = """CREATE TABLE DONATOR (D_ID char(7) NOT NULL, EMAIL varchar(50) NOT NULL, PRIMARY KEY(EMAIL), FOREIGN KEY (D_ID, EMAIL) REFERENCES PERSON (ID, EMAIL)) ON DELETE CASCADE"""

queryCreateOrganizorTable = """CREATE TABLE ORGANIZOR (O_ID char(7) NOT NULL, EMAIL varchar(50) NOT NULL, PRIMARY KEY(EMAIL), FOREIGN KEY (O_ID, EMAIL) REFERENCES PERSON (ID, EMAIL)) ON DELETE CASCADE"""

queryCreateVolunteerTable = """CREATE TABLE VOLUNTEER (V_ID char(7) NOT NULL, EMAIL varchar(50) NOT NULL, STATUS varchar(20), VOLUNTARY char(100), PRIMARY KEY(EMAIL), FOREIGN KEY (V_ID, EMAIL) REFERENCES PERSON (ID, EMAIL)) ON DELETE CASCADE"""

queryCreateEventTable = """CREATE TABLE EVENT (Event_Name varchar(80) NOT NULL, Start_Time date NOT NULL, End_Time date NOT NULL, Location varchar(40) NOT NULL, Budget int NOT NULL, Shop varchar(40) NOT NULL, Items varchar(40) NOT NULL, Quantity int, Event_for varchar(40), Event_id char(100), Created_by varchar(100), PRIMARY KEY(Event_id), FOREIGN KEY(Created_by)REFERENCES ORGANIZOR (EMAIL)) ON DELETE CASCADE"""

queryCreateDonateTable = """CREATE TABLE DONATE (D_ID char(7) NOT NULL, Event_id char(100) NOT NULL, PAYMENT_DETAILS varchar(20) NOT NULL, PAYMENT varchar(20) not null, FOREIGN KEY(Event_id) REFERENCES EVENT(Event_id)) ON DELETE CASCADE"""

queryCreateFundTable = """CREATE TABLE FUND (EVENT_ID char(100) NOT NULL, COLLECTED_AMOUNT int, Fund_Status varchar(10), FUND_TAKEN_BY varchar(100), PRIMARY KEY(EVENT_ID), FOREIGN KEY(EVENT_ID) REFERENCES EVENT(Event_id)) ON DELETE CASCADE"""


queryInsertAdminData = "INSERT INTO PERSON (FIRST_NAME, LAST_NAME, EMAIL, CONTACT, NID, PASSWORD, ID) VALUES ('Abdullah', 'Khondoker', 'abdullahkhondoker201@gmail.com', '01729922119', '1122334455', '0000','A')"

queryCreateShopTable = """CREATE TABLE SHOP (Shop_Name varchar(50) NOT NULL, EVENT_ID char(100) NOT NULL, PAY_DEMAND varchar(20) NOT NULL, DELIVERY_STATUS varchar(30) NOT NULL,PRIMARY KEY(Shop_Name,EVENT_ID),FOREIGN KEY(EVENT_ID) REFERENCES EVENT(EVENT_ID)) ON DELETE CASCADE"""

cur.execute(queryInsertAdminData)
con.close
con.commit()
print('Success')

