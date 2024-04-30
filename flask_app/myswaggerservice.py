from flask import jsonify, request
from datetime import datetime
import pyodbc
import bcrypt
import os

class MySwaggerService:
    # accessing environment variables 
    # for SQL DB connection and password_salt for password creation and verification 
    conn_str = os.environ.get('DB_CONNECTION')
    password_salt = os.environ.get('PW_SALT').encode('utf-8') 
    
    # static password salt so that password salt is the same 
    # for every created password can be retrieved easily for verification
    salt =  bcrypt.gensalt()
    password_salt = salt
    
    # open SQL Connection
    def open_sql(self):
        # if connection is closed, open it
        if self.conn.closed:
            conn = os.environ.get('DB_CONNECTION')    
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
    
    # check if email exist in database

    def check_duplicate(self, email, conn): 
        # create cursor object
        cursor = conn.cursor()
        
        # get email from the database
        sql_get_email_query = "EXEC spShopper_GetEmail ?"
        cursor.execute(sql_get_email_query, email)
        
        #fetch the row tuple
        email_result = cursor.fetchone()
        
        # if email does not exist, return true - customer can add their info to the databse
        if (email_result is not None and isinstance(email_result[0], str)):
            return True
        else:
            return False
        
        
    
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
        
    # display all customers
    def display_all_customers(self):
        # get customer details
        rows = self.get_all_customers()
        
        # show customers
        customers = self.show_customers(rows)
        
        return customers
    
    def check_authentication(self, cursor, email, password):
        # compare bytes password with hashed_password in the database
        sql_customer_getpassword = "EXEC spShopper_GetPassword ?"
        cursor.execute(sql_customer_getpassword, (email))
        
        # get the password hash in the database
        password_hash_obj = cursor.fetchone()
    
        # if password_hash does exist, email is valid
        if (password_hash_obj is not None and isinstance(password_hash_obj[0], str)):
            # access password hash element
            hashed_password = password_hash_obj[0]
            # convert to bytes
            hashed_password_bytes = hashed_password.encode('utf-8')
            # compare password with password hash
            if (bcrypt.checkpw(password, hashed_password_bytes)):
                # password is the same
                return True
            else:
                #password is not the same
                return False
        else:
            return False
    
    def show_customer(self, conn, cursor, email):
          # get customer info from the databse, given the email
            sql_customer_getall = "EXEC spShopper_GetAll ?"
            cursor.execute(sql_customer_getall, (email))
            
            #get customer data
            data = cursor.fetchone()
            
            # if there is a data, display it
            if (data != None):
            
                customer_detail = {
                'customer_id': data.pk_shopper_id,   
                'first_name': data.first_name,
                'last_name': data.last_name,
                'email_address': data.email,
                'mobile_phone': data.phone,
                'created_date': data.created_date,
                'modified_date': data.modified_date
                }
                
                conn.commit()
                
                # return customer detail
                return customer_detail
            else:
                # return a null customer data
                return data

            
    # display customer info based on email and password
    def display_customer(self, email, password):
        
        # open and close SQL database connection
        with pyodbc.connect(self.conn_str) as conn:
            
            # create cursor object
            cursor = conn.cursor()
            
            #check email & password
            is_authentication_valid = self.check_authentication(cursor, email, password)
          
            # if email & password valid, display customer info
            if(is_authentication_valid):
                # display customer
                data = self.show_customer(conn, cursor, email)
                return data
            else:
                # email or password is not valid
                data = None
                return data 
          
    
    def add_customer(self, first_name, last_name, email, password, phone_number):
        
        # open and close database connection
        with pyodbc.connect(self.conn_str) as conn:
            
            # default params
            created_date = datetime.now()
            modified_date = None
            
            # convert password to hash + static salt via bcrypt algorithm
            password_hash = bcrypt.hashpw(password, self.password_salt)
            
            # check if email exist in the database. 
            # If it is exist, customer cannot add same email
            is_exist = self.check_duplicate(email, conn)
            
            if (is_exist == True):
                return jsonify({'error': 'An email already exist in the database. Customer cannot add the same email'}), 409
            
            # default params
            created_date = datetime.now()
            modified_date = None
            
            # convert password to hash + static salt via bcrypt algorithm
            password_hash = bcrypt.hashpw(password, self.password_salt)
            
            # create cursor object
            cursor = conn.cursor()
            
            try:
                sql_customer_insert_query = "EXEC spShopper_InsertAll ?, ?, ?, ?, ?, ?, ?"
                cursor.execute(sql_customer_insert_query, (first_name, last_name, email, phone_number, created_date, modified_date, password_hash))
                conn.commit()
                
                # close SQL cursor & connection
                self.close_sql(cursor)
                
                return jsonify({'message': 'Customer\'s profile added successfully'}), 200
            except Exception as e:
                
                # close SQL cursor & connection
                self.close_sql(cursor)
                
                error_message = "There was an issue adding customer's info: " + str(e)
                return jsonify({'error': error_message}), 500