from flask import jsonify, request
from datetime import datetime
import pyodbc

class MySwaggerService:
    # static SQL conection
    conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};' 'Server=(localdb)\MSSQLLocalDB;' 'Database=account_receivable;' 'Trusted_Connection=yes;')
    
    # open SQL Connection
    def open_sql(self):
        # if connection is closed, open it
        if self.conn.closed:
            conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};' 'Server=(localdb)\MSSQLLocalDB;' 'Database=account_receivable;' 'Trusted_Connection=yes;')
            return conn
        else:
            # if connection open, return it
            return self.conn
            
        
    # close SQL close and cursor        
    def close_sql(self, cursor):
        # if cursor open, close it
        if cursor:
            cursor.close()
        else:
         self.conn.close()
        
    # get customer details
    def get_all_customers(self):
        
        # open SQL connection
        conn = self.open_sql()
        
        # Create a cursor object
        cursor = conn.cursor()
        sql_get_all_customer_details = "EXEC spCustomerTrial_GetAll"
        
        cursor.execute(sql_get_all_customer_details)
        
        # Fetch all rows from the cursor
        rows = cursor.fetchall()
        
        # close SQL cursor and conn
        self.close_sql(cursor)
        
        # return rows of customer details    
        return rows
    
    # show customers
    def show_customers(self, rows):
        try: 
            # open SQL connection
            conn = self.open_sql()
            # Create a list to store customer details
            customers = []
            
            #Iterate through rows of customer details
            for row in rows:
                customer = {
                    'customer_id': row.pk_customer_id,   
                    'first_name': row.first_name,
                    'last_name': row.last_name,
                    'email_address': row.email_address,
                    'mobile_phone': row.mobile_phone,
                    'created_date': row.created_date,
                    'modified_date': row.modified_date
                }
                customers.append(customer)
            
            conn.commit()
            
            # close SQL connection
            conn.close()
            
            # reurn all customers
            return customers
        except:
            # close SQL connection
            conn.close()
            
            # return customers None if fail
            return customers    
    
    # Insert customer's phone number
    def add_phone(self, phone_number, created_date, modified_date):       
        try:
            # open SQL connectiom
            conn = self.open_sql()
            
            # create cursor obj
            cursor = conn.cursor()
            
            # insert phone
            sql_phone_insert_query = "EXEC spMobilePhoneTrial_InsertAll ?, ?, ?"
            cursor.execute(sql_phone_insert_query, (phone_number, created_date, modified_date))
            conn.commit()
            
            # close SQL cursor & connection
            self.close_sql(cursor)
            
            message = 'Customer\'s phone number added successfully'
            return jsonify({'message': message}), 200
        except Exception as e:
            # close SQL cursor & connection
            self.close_sql(cursor)
            
            error_message = "There was an issue adding customer's phone number: " + str(e)
            return jsonify({'error': error_message}), 500
    
    def add_email(self, email, created_date, modified_date):
        try:
            # open SQL Connection
            conn = self.open_sql()
            
            # create cursor object
            cursor = conn.cursor()
             
            sql_email_insert_query = "EXEC spEmailAddressTrial_InsertAll ?, ?, ?"
            cursor.execute(sql_email_insert_query, (email, created_date, modified_date))
            conn.commit()
            
            # close SQL cursor & connection
            self.close_sql(cursor)
            message = 'Customer\'s email added successfully'
            return jsonify({'message': message}), 200
        
        except Exception as e:
            # close SQL cursor & connection
            self.close_sql(cursor)
            
            error_message = "There was an issue adding customer's phone number: " + str(e)
            return jsonify({'error': error_message}), 500
        
    # add customer's names
    def add_name(self, first_name, last_name, email_id, phone_number_id, created_date, modified_date):
        # open SQL connection
        conn = self.open_sql()
        
        # create cursor object
        cursor = conn.cursor()
        
        try:
            sql_customer_insert_query = "EXEC spCustomerTrial_InsertAll ?, ?, ?, ?, ?, ?"
            cursor.execute(sql_customer_insert_query, (first_name, last_name, email_id, phone_number_id, created_date, modified_date))
            conn.commit()
             
            # close SQL cursor & connection
            self.close_sql(cursor)
            
            return jsonify({'message': 'Customer\'s profile added successfully'}), 200
        except Exception as e:
            
            # close SQL cursor & connection
            self.close_sql(cursor)
            
            error_message = "There was an issue adding customer's info: " + str(e)
            return jsonify({'error': error_message}), 500
    
    # get customer's email by ID
    def get_email(self, email_id):
        
        # open SQL Connection
        conn = self.open_sql()
        
        # create cursor object
        cursor = conn.cursor()
        
        sql_customer_get_email_byid_query = "EXEC spEmailAddressTrial_GetById ?"
        cursor.execute(sql_customer_get_email_byid_query, (email_id))
        email = cursor.fetchone()
        
        return email
    
    # get customer's phone by ID
    def get_phone(self, phone_number_id):
        
        # open SQL connection
        conn = self.open_sql()
        
        # create cursor object
        cursor = conn.cursor()
        
        sql_customer_get_phone_byid_query = "EXEC spPhoneNumberTrial_GetById ?"
        cursor.execute(sql_customer_get_phone_byid_query, (phone_number_id))
        phone = cursor.fetchone()
        
        return phone
        
    # display all customers
    def display_all_customers(self):
        # get customer details
        rows = self.get_all_customers()
        
        # show customers
        customers = self.show_customers(rows)
        
        return customers
    
    # display customer info based on customer ID
    def display_customer(self, customer_id):
        # open SQL connection
        conn = self.open_sql()
        # create a customer object
        cursor = conn.cursor()
        
        #Execute query
        sql_customer_getbyid = "EXEC spCustomerTrial_GetById ?"
        cursor.execute(sql_customer_getbyid, (customer_id))
        
        #get customer data
        data = cursor.fetchone()
        
        # if there is a data, display it
        if (data != None):
        
            customer_detail = {
            'customer_id': data.pk_customer_id,   
            'first_name': data.first_name,
            'last_name': data.last_name,
            'email_address': data.email_address,
            'mobile_phone': data.mobile_phone,
            'created_date': data.created_date,
            'modified_date': data.modified_date
            }
            
            conn.commit()
            
            # close sql cursor and connection
            self.close_sql(cursor)
            
            # return customer detail
            return customer_detail
        else:
            # close sql cursor and connection
            self.close_sql(cursor)
            
            # return a null customer data
            return data
    
    def add_customer_phone(self, phone_number):
        
        if (phone_number is not None):
            # default params
            created_date = datetime.now()
            modified_date = None
              
            # add phone
            message = self.add_phone(phone_number, created_date, modified_date)
            
            return message
        else:
            message = 'Phone parameter is missing'
            return message
        
    def add_customer_email(self, email):
        
        if (email is not None):
             # default params
            created_date = datetime.now()
            modified_date = None
              
            # add phone
            message = self.add_email(email, created_date, modified_date)
            
            return message
        else:
            message = 'Email parameter is missing'
            return message
    
    def add_customer(self, first_name, last_name, email_id, phone_number_id):
        
        # get the email by ID from the database
        email = self.get_email(email_id)
        
        #get the phone_number by ID from the database
        phone_number = self.get_phone(phone_number_id)
        
        # if the email and phone_number is not found, return jsonify error
        if email is None:
            return jsonify({'error': f'Customer\'s email by email_id {email_id} is not found'}), 400
        elif phone_number is None:
            return jsonify({'error': f'Customer\'s phone number by phone_number_id {phone_number_id} is not found'}), 400
        
        if first_name and last_name is not None:
            # default params
            created_date = datetime.now()
            modified_date = None
        
            # insert customer's name
            message = self.add_name(first_name, last_name, email_id, phone_number_id, created_date, modified_date)
            
            return message 
            
        else:
            return jsonify({'error': 'one of the parameter is missing'}), 400
        