from flask import jsonify
from datetime import datetime
import pyodbc
import bcrypt
import os

class MySwaggerService:
    # accessing environment variables for SQL DB connection 
    conn_str = os.environ.get('DB_CONNECTION')
    
        
    # check if email exist in database
    def check_email_duplicate(self, email, conn): 
        # create cursor object
        cursor = conn.cursor()
        
        # get email from the database
        sql_get_email_query = "EXEC spShopper_GetEmail ?"
        cursor.execute(sql_get_email_query, email)
        
        #fetch the row tuple
        email_result = cursor.fetchone()
        
        # if email exist, return true - customer can add their info to the databse
        if (email_result is not None and isinstance(email_result[0], str)):
            return True
        else:
            return False
    
    def is_customer_id_exist(self, customer_id, conn):
        # create cursor object
        cursor = conn.cursor()
        
        # get customer_id from the database
        sql_get_customer_id_query = "SELECT pk_shopper_id FROM shopper WHERE pk_shopper_id = ?"
        cursor.execute(sql_get_customer_id_query, (customer_id,))
        
        #fetch the row tuple
        customer_id_result = cursor.fetchone()
        
        # if customer_id exist, return true
        if (customer_id_result is not None and isinstance(customer_id_result[0], int)):
            return True
        else:
            return False
        
    # display all products from the database
    def show_products(self, conn, cursor):
        try:
            sql_get_all_products = "EXEC spProduct_GetAll"
        
            cursor.execute(sql_get_all_products)
            
            # Fetch all rows from the cursor
            rows = cursor.fetchall()
            
            # Create a list to store products
            products = []
            
            #Iterate through rows of products
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
            
            # reurn all products
            return jsonify({'message': "All products displayed successfully", 'data': products}), 200
        
        except Exception as e:
            error_message = "There was an issue displaying all products " + str(e)
            return jsonify({'error': error_message}), 500
        
    # verify user's email and password   
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
    
    # display customer's profile
    def show_customer(self, conn, cursor, email):
        try:
            # get customer info from the databse, given the email
            sql_customer_getall = "EXEC spShopper_GetAll ?"
            cursor.execute(sql_customer_getall, (email))
            
            #get customer data
            data = cursor.fetchone()
            
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
            return jsonify({'message': "Customer's profile displayed successfully", 'data': customer_detail}), 200
        
        except Exception as e:
            # return error message
            error_message = "There was an issue displaying customer's profile: " + str(e)
            return jsonify({'error': error_message}), 500

    # displayed all products based on verified email and password
    def display_products(self, email, password):
        # open and close SQL database connection
        with pyodbc.connect(self.conn_str) as conn:
            # create cursor object
            cursor = conn.cursor()
            
            #check email & password
            is_authentication_valid = self.check_authentication(cursor, email, password)
          
            # if email & password valid, display products
            if(is_authentication_valid):
                # display products
                return self.show_products(conn, cursor)
            else:
               # either email or password is not valid
               return jsonify({'error': 'either email or password is not valid'}), 400  
            
    # display customer info based on verified email and password
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
                return self.show_customer(conn, cursor, email)
                    
            else:
                # either email or password is not valid
                return jsonify({'error': 'either email or password is not valid'}), 400
          
    # add customer to the database
    def add_customer(self, first_name, last_name, email, password, phone_number):
        # open and close database connection
        with pyodbc.connect(self.conn_str) as conn:
            
            # check if email exist in the database. 
            # If it is exist, customer cannot add same email
            is_exist = self.check_email_duplicate(email, conn)
            
            if (is_exist == True):
                return jsonify({'error': 'An email already exist in the database. Customer cannot add the same email'}), 409
            
            # default params
            created_date = datetime.now()
            modified_date = None
            
            # convert password to hash + static salt via bcrypt algorithm
            password_salt = bcrypt.gensalt()
            password_hash = bcrypt.hashpw(password, password_salt)
            
            # create cursor object
            cursor = conn.cursor()
            
            try:
                sql_customer_insert_query = "EXEC spShopper_InsertAll ?, ?, ?, ?, ?, ?, ?"
                cursor.execute(sql_customer_insert_query, (first_name, last_name, email, phone_number, created_date, modified_date, password_hash))
                conn.commit()
                
                return jsonify({'message': 'Customer\'s profile added successfully'}), 200
            except Exception as e:
                
                # close SQL cursor & connection
                self.close_sql(cursor)
                
                error_message = "There was an issue adding customer's info: " + str(e)
                return jsonify({'error': error_message}), 500
    
    def add_customer_order(self, customer_id):
        # open and close database connection
        with pyodbc.connect(self.conn_str) as conn:
           
            # check if customer's id exist in the database
            is_exist = self.is_customer_id_exist(customer_id, conn)
            
            if (is_exist == False):
                return jsonify({'error': 'Customer\'s id does not exist'}), 409
            
             # default params
            created_date = datetime.now()
            modified_date = None
            
            # create cursor object
            cursor = conn.cursor()
            
            try:
                sql_customer_id_insert_query = "INSERT INTO orders VALUES (?, ?, ?)"
                cursor.execute(sql_customer_id_insert_query, (customer_id, created_date, modified_date))
                conn.commit()
                
                return jsonify({'message': 'Customer\'s id is added successfully'}), 200
            
            except Exception as e:
                
                # close SQL cursor & connection
                self.close_sql(cursor)
                
                error_message = "There was an issue adding customer's id: " + str(e)
                return jsonify({'error': error_message}), 500
    
             
        