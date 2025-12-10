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
    
    def is_order_id_exist(self, order_id, conn):
        # create cursor object
        cursor = conn.cursor()
        
        # get order id from the database
        sql_get_order_id_query = "SELECT pk_order_id FROM order_record WHERE pk_order_id = ?"
        cursor.execute(sql_get_order_id_query, (order_id,))
        
        # fetch the row tuple
        order_id_result = cursor.fetchone()
        
        # if order_id exist, return true
        if (order_id_result is not None and isinstance(order_id_result[0], int)):
            return True
        else:
            return False
    
    def is_product_exist(self, product_id, unit_price, quantity, conn):
        # create cursor object
        cursor = conn.cursor()
        
        # get product id from the database
        sql_get_product_id_query = "SELECT pk_product_id FROM product WHERE pk_product_id = ? AND product_price = ? AND in_stock_quantity = ?"
        cursor.execute(sql_get_product_id_query, (product_id,unit_price, quantity))
        
        # fetch the row tuple
        product_id_result = cursor.fetchone()
        
        # if product_id exist, return true
        if (product_id_result is not None and isinstance(product_id_result[0], int)):
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
    def get_customer(self, conn, cursor, customer_id):
        try:
            # get customer detail from the databse, given the customer id
            sql_customer_getall = "SELECT pk_shopper_id, first_name, last_name, email, phone, created_date, modified_date FROM shopper WHERE pk_shopper_id = ?"
            cursor.execute(sql_customer_getall, (customer_id))
            
            # get customer data
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
    def display_customer(self, customer_id):
        # open and close SQL database connection
        with pyodbc.connect(self.conn_str) as conn:
            # create cursor object
            cursor = conn.cursor()
            
            #check customer_id
            is_exist = self.is_customer_id_exist(customer_id, conn)
          
            # if customer_id exist, display customer info
            if(is_exist):
                # display customer
                return self.get_customer(conn, cursor, customer_id)
                    
            else:
                # either email or password is not valid
                return jsonify({'error': 'customer_id is not valid'}), 400
          
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
    
    def add_customer_order(self, customer_id, subtotal, shipping_fee, total_amount):
        # open and close database connection
        with pyodbc.connect(self.conn_str) as conn:
           
            # check if customer's id exist in the database
            is_exist = self.is_customer_id_exist(customer_id, conn)
            
            if (is_exist == False):
                return jsonify({'error': 'Customer\'s id does not exist'}), 404
            
            # default params
            order_date = datetime.now()
            payment_status = "Paid" # assume all customers have a "Paid" status for now, for simplicity.
            created_date = datetime.now()
            modified_date = None
            
            # create cursor object
            cursor = conn.cursor()
            
            try:
                sql_customer_id_insert_query = "INSERT INTO order_record VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
                cursor.execute(sql_customer_id_insert_query, (customer_id, order_date, subtotal, shipping_fee, total_amount, payment_status, created_date, modified_date))
                conn.commit()
                
                return jsonify({'message': 'Order record is added successfully'}), 200
            
            except Exception as e:
                
                error_message = "There was an issue adding customer's id: " + str(e)
                return jsonify({'error': error_message}), 500
    
    def add_customer_order_item(self, order_id, product_id, unit_price, quantity):
        # open and close database connection
        with pyodbc.connect(self.conn_str) as conn:
            
            is_order_id_exist = self.is_order_id_exist(order_id, conn)
            is_product_exist = self.is_product_exist(product_id, unit_price, quantity, conn)
            
            if (is_order_id_exist == False or is_product_exist == False):
                return jsonify({'error': 'Either order\'s id does not exist or product does not exist'}), 404
            
            # default params
            created_date = datetime.now()
            modified_date = None
            
            # create cursor object
            cursor = conn.cursor()
            
            try:
                sql_order_insert_query = "INSERT INTO order_item VALUES (?, ?, ?, ?, ?, ?)"
                cursor.execute(sql_order_insert_query, (order_id, product_id, quantity, unit_price, created_date, modified_date))
                conn.commit()
                
                return jsonify({'message': 'Order item is added successfully'}), 200
            
            except Exception as e:
                
                error_message = "There was an issue adding an order item: " + str(e)
                return jsonify({'error': error_message}), 500
            
     
    
    def add_customer_payment(self, customer_id, order_id, total_price, payment_token, last_4_digits, card_type):
        # open and close database connection
        with pyodbc.connect(self.conn_str) as conn:
            is_customer_id_exist = self.is_customer_id_exist(customer_id, conn)
            is_order_id_exist = self.is_order_id_exist(order_id, conn)
            
            if (is_customer_id_exist == False or is_order_id_exist == False):
                return {'error': 'Either customer\'s id does not exist or order\'s id does not exist'}, 404       
            
            # default params
            payment_status = "Paid" # assume all customers have a "Paid" status for now, for simplicity
            created_date = datetime.now()
            
            # create cursor object
            cursor = conn.cursor()
            
            try:
                sql_payment_insert_query = "INSERT INTO payment VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
                cursor.execute(sql_payment_insert_query, (customer_id, order_id, total_price, payment_status, payment_token, last_4_digits, card_type, created_date))
                conn.commit()
                
                return {'message': 'payment info is added successfully', 'order_id': order_id}, 200
            
            except Exception as e:
                
                error_message = "There was an issue adding payment info: " + str(e)
                return {'error': error_message}, 500
    
    def get_payment_info(self, order_id):
      with pyodbc.connect(self.conn_str) as conn:
        # create cursor object
        cursor = conn.cursor()
        
        sql_get_payment = "SELECT card_type, last_4_digits FROM payment WHERE fk_order_id = ?"
        cursor.execute(sql_get_payment, (order_id,))
                
        # get payment
        data = cursor.fetchone()
        payment_info = {
            'card_type': data.card_type,
            'last_4_digits': data.last_4_digits
        }
        
        conn.commit()
        return payment_info
      
    def get_payment(self, order_id):
      with pyodbc.connect(self.conn_str) as conn:
            # create cursor object
            cursor = conn.cursor()
            
            # get order id
            sql_get_order_id = "SELECT fk_order_id FROM payment WHERE fk_order_id = ?"
            cursor.execute(sql_get_order_id, (order_id,))
            
            result = cursor.fetchone()
            
            if result is not None:
                # get order id
                order_id = result[0]
                
                if isinstance(order_id, int):
                    try:
                        return self.get_payment_info(order_id)
                    except Exception as e:
                        error_message = "There was an issue getting payment info: " + str(e)
                        return {'error': error_message}, 500
                else:
                    # order_id is not valid
                    return jsonify({'error': 'order_id is not valid'}), 400
            else:
                return jsonify({'error': "Invalid order id"}), 404       
    
   