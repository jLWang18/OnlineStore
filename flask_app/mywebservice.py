from flask import jsonify
from datetime import datetime, timedelta
import pyodbc
import bcrypt
import os

class MyWebService:
  # accessing environment variables for SQL DB connection 
  conn_str = os.environ.get('DB_CONNECTION')
  
  # close sql cursor & Connection
  def close_sql(self, cursor):
      # if cursor open, close it
    if cursor:
        cursor.close()
    else:
        self.conn.close()
        
  # add customer email
  def add_customer_email(self, email, created_date, modified_date):    
      try:
        # first add email to the email table
        sql_email_insert_ui_query = "EXEC spEmailAddressTrial_InsertAll ?, ?, ?"
        
        # create a cursor object
        cursor = self.conn.cursor()
        
        cursor.execute(sql_email_insert_ui_query, (email, created_date, modified_date))
        self.conn.commit()
        
        # close cursor and connection
        self.close_sql(cursor)
        
        return True
    
      except Exception:
         # close cursor and connection
        self.close_sql(cursor)
        
        return False
  
  def add_customer_phone(self, phone, created_date, modified_date):
      try:
        # second add phone to the phone table
        sql_phone_insert_ui_query = "EXEC spMobilePhoneTrial_InsertAll ?, ?, ?"
        
        # create cursor object
        cursor = self.conn.cursor()
        
        cursor.execute(sql_phone_insert_ui_query, (phone, created_date, modified_date))
        self.conn.commit()
        
        return True
      except Exception:
            # close cursor and connection
            self.close_sql(cursor)
            
            return False
    
    # get email id from the database
  def get_email_id(self, email):
        
    email_id = None
    
    sql_customer_get_email_byid_query = "EXEC spEmailAddressTrial_GetIdByEmail ?"
    # create cursor object
    cursor = self.conn.cursor()
    cursor.execute(sql_customer_get_email_byid_query, (email))
    
    #fetch the row tuple
    result = cursor.fetchone()
    
    # check if result is not None and is an integer
    if result is not None and isinstance(result[0], int):
        # assigned the first tuple value to email id
        email_id = result[0]
        
        return email_id
    else:
        # close cursor and connection
        self.close_sql(cursor)
        
        print("Error: email_id is not an integer or is None")

  #get phone id from the database
  def get_phone_id(self, phone):
      phone_id = None
      
      sql_customer_get_phone_byid_query = "EXEC spMobilePhoneTrial_GetIdByPhone ?"
      
      # create cursor object
      cursor = self.conn.cursor()
      cursor.execute(sql_customer_get_phone_byid_query, (phone))
      
      #fetch the row tuple
      result = cursor.fetchone()
      
      # check if result is not None and is an integer
      if result is not None and isinstance(result[0], int):
          # assigned the first tuple value to phone id
          phone_id = result[0]
          return phone_id
      
      else:
          # close cursor and connection
          self.close_sql(cursor)
          
          print("Error: phone_id is not an integer or None")
  
    # add customer's first and last names
  def add_customer_name(self, first_name, last_name, email_id, phone_id, created_date, modified_date):
      
      try:
          sql_customer_insert_ui_query = "EXEC spCustomerTrial_InsertAll ?, ?, ?, ?, ?, ?"
          
          # create cursor obj
          cursor = self.conn.cursor()
          cursor.execute(sql_customer_insert_ui_query, (first_name, last_name, email_id, phone_id, created_date, modified_date))
          self.conn.commit()
            
          # return sucess message
          message = "Success: customer added successfully"
            
          # close cursor and connection
          self.close_sql(cursor)
            
          return message
    
      except Exception as e:
          # return error message
           error_message = "There is an error in adding customer: " + str(e)
            
           # close cursor and connection
           self.close_sql(cursor)
        
           return error_message
  
   # submit customer info logic
  def add_customer(self, first_name, last_name, email, phone, created_date, modified_date):
      # add customer email to the database and check if added successfully
      is_email_valid = self.add_customer_email(email, created_date, modified_date)
            
      # add customer phone to the database and check if added successfully
      is_phone_valid = self.add_customer_phone( phone, created_date, modified_date)
            
      # get the email id from the database
      email_id = self.get_email_id (email)
        
      # get the phone_id from the database
      phone_id = self.get_phone_id(phone)
        
      # add first name, last name, email, and phone to the database 
      if is_email_valid and is_phone_valid:
          message = self.add_customer_name(first_name, last_name, email_id, phone_id, created_date, modified_date)
          return message
      else:
          # display err message: email input or phone input is not valid
          return "Customer's email and/or phone is not valid"
  
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
            
  def authenticate_customer_ui(self, email, password):
         # open and close SQL database connection
        with pyodbc.connect(self.conn_str) as conn:
            # create cursor object
            cursor = conn.cursor()
            
            #check email & password
            is_authentication_valid = self.check_authentication(cursor, email, password)
            
            return is_authentication_valid
                          
  # display products
  def show_products_ui(self):
       # open and close SQL database connection
        with pyodbc.connect(self.conn_str) as conn:
            # create cursor object
            cursor = conn.cursor()
            
            # call SP to retrieve data
            sql_get_all_products = "EXEC spProduct_GetAll"
        
            cursor.execute(sql_get_all_products)
            
            # Fetch all rows from the cursor
            rows = cursor.fetchall()
            
            # Create a list to store products
            products = []
            
            # Iterate through rows of products
            for row in rows:
                product = {
                    'product_id': row.pk_product_id,   
                    'product_category': row.product_category,
                    'product_name': row.product_name,
                    'product_price': row.product_price,
                    'in_stock_quantity': row.in_stock_quantity,
                    'created_date': row.created_date,
                    'modified_date': row.modified_date
                    }
                products.append(product)
            
            conn.commit()
            
        # diplay products    
        return products
    
  
  def add_token(self, shopper_id, access_token):
      # open and close SQL database connection
       with pyodbc.connect(self.conn_str) as conn:
           # default params
           now = datetime.now()
           
           # when the token first created, the issue date is the current datetime and expires at 2 weeks from now
           issued_at = now
           expires_at = now + timedelta(weeks=2)
           last_used_at = now
           is_revoked = 0 
           
                      
           # create cursor object
           cursor = conn.cursor()
           
           try:
               # Insert query
               sql_add_token = "INSERT INTO access_token values (?, ?, ?, ?, ?, ?)"
               
               cursor.execute(sql_add_token, (shopper_id, access_token, issued_at, expires_at, last_used_at, is_revoked))
               conn.commit()
               
               #return jsonify({'message': 'access token was added successfully'}), 200
               
               # return access token when successfully added to the database 
               return access_token
           
           except Exception as e:
                error_message = "There was an issue in adding access token: " + str(e)
                return jsonify({'error': error_message}), 500
               
               
      
  def get_shopper_id(self, email):
       # open and close SQL database connection
       with pyodbc.connect(self.conn_str) as conn:
           # create cursor object
           cursor = conn.cursor()
           
           # call SP to get shopper ID
           sql_get_id = "EXEC spShopper_GetId ?"
           cursor.execute(sql_get_id, (email))
           
           # get result
           result = cursor.fetchone()
           
          # check if result is not None and is an integer
           if result is not None and isinstance(result[0], int):
               # assigned the first tuple value to shopper id
               shopper_id = result[0]
               return shopper_id
           else:
              return jsonify({"error: there is an issue in getting shopper id"}, 500)
    
  def  get_customer_name(self, access_token):
       # open and close SQL database connection
       with pyodbc.connect(self.conn_str) as conn:
           # create cursor object
           cursor = conn.cursor()
           
           # get shopper id
           sql_get_shopper_id = "SELECT fk_shopper_id FROM access_token WHERE token = ?"
           cursor.execute(sql_get_shopper_id, (access_token,))
           
            # get result
           result = cursor.fetchone()
           
           # check if result is not None and is an integer
           if result is not None:
               # get shopper id
               shopper_id = result[0]
               
               if isinstance(shopper_id, int):
                   
                   try:
                        sql_get_customer_data = "SELECT first_name FROM shopper WHERE pk_shopper_id = ?"
                        cursor.execute(sql_get_customer_data, (shopper_id,))
                    
                        # get customer's first name
                        result = cursor.fetchone()
                        
                        if result is not None:
                            print(f"Customer's first name: {result[0]}")
                            
                            return jsonify({'data': result[0]}), 200
                        else:
                            return jsonify({'error': 'Customer not found'}), 404
                    
                   except Exception as e:
                        error_message = "There was an issue in getting username " + str(e)
                        return jsonify({'error': error_message}), 500
               else:
                  return jsonify({"error": "Shopper ID is not valid"}), 400 
               
           else:
              return jsonify({"error": "Invalid access token or shopper ID not found"}), 404 
              
             
        