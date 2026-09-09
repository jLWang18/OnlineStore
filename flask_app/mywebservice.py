from flask import jsonify
from datetime import datetime, timedelta
import pyodbc
import bcrypt
import os

class MyWebService:
    # accessing environment variables for SQL DB connection
    conn_str = os.environ.get('DB_CONNECTION')
    
    # shipping fee of an order
    SHIPPING_COST = 4.99

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
        cursor.execute(sql_customer_get_email_byid_query, (email,))

        #fetch the row tuple
        result = cursor.fetchone()

        # check if result is not None and is an integer
        if result is not None and isinstance(result[0], int):
            # assigned the first tuple value to email id
            email_id = result[0]
            # close cursor and connection
            self.close_sql(cursor)

            return email_id
        else:
            # close cursor and connection
            self.close_sql(cursor)

            print("Error: email_id is not an integer or is None")
            return None

    #get phone id from the database
    def get_phone_id(self, phone):
        phone_id = None

        sql_customer_get_phone_byid_query = "EXEC spMobilePhoneTrial_GetIdByPhone ?"

        # create cursor object
        cursor = self.conn.cursor()
        cursor.execute(sql_customer_get_phone_byid_query, (phone,))

        #fetch the row tuple
        result = cursor.fetchone()

        # check if result is not None and is an integer
        if result is not None and isinstance(result[0], int):
            # assigned the first tuple value to phone id
            phone_id = result[0]
            # close cursor and connection
            self.close_sql(cursor)
            return phone_id

        else:
            # close cursor and connection
            self.close_sql(cursor)

            print("Error: phone_id is not an integer or None")
            return None

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

    # check if email exist in database
    def check_duplicate(self, email, conn):
        # create cursor object
        cursor = conn.cursor()

        # get email from the database
        sql_get_email_query = "EXEC spShopper_GetEmail ?"
        cursor.execute(sql_get_email_query, (email,))

        # fetch the row tuple
        email_result = cursor.fetchone()

        # if email does not exist, return true - customer can add their info to the databse
        if (email_result is not None and isinstance(email_result[0], str)):
            return True
        else:
            return False

    # add customer to the database
    def add_customer(self, first_name, last_name, email, password, phone_number):
        # open and close database connection
        with pyodbc.connect(self.conn_str) as conn:
            # default params
            created_date = datetime.now()
            modified_date = None

            # check if email exist in the database.
            # If it is exist, customer cannot add same email
            is_exist = self.check_duplicate(email, conn)

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

    def check_authentication(self, cursor, email, password):
        # compare bytes password with hashed_password in the database
        sql_customer_getpassword = "EXEC spShopper_GetPassword ?"
        cursor.execute(sql_customer_getpassword, (email,))

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

    # get products
    def get_products(self):
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

        # get products
        return products

    def is_customer_id_exist(self, customer_id, conn):
        # create cursor object
        cursor = conn.cursor()

        sql_get_customer_id = "SELECT pk_shopper_id FROM shopper WHERE pk_shopper_id = ?"
        cursor.execute(sql_get_customer_id, (customer_id))

        result = cursor.fetchone()

        # if customer_id exist, return True
        if result is not None and isinstance(result[0], int):
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
    
    def is_product_exist(self, product_id, conn):
        # create cursor object
        cursor = conn.cursor()
        
        # get product id from the database
        sql_get_product_id_query = "SELECT pk_product_id FROM product WHERE pk_product_id = ?"
        cursor.execute(sql_get_product_id_query, (product_id,))
        
        # fetch the row tuple
        product_id_result = cursor.fetchone()
        
        # if product_id exist, return true
        if (product_id_result is not None and isinstance(product_id_result[0], int)):
            return True
        else:
            return False
    
    def get_customer_detail(self, conn, cursor, customer_id):
        # get customer detail from the databse, given the customer id
        sql_get_customer = "SELECT pk_shopper_id, first_name, last_name, email, phone, created_date, modified_date FROM shopper WHERE pk_shopper_id = ?"
        cursor.execute(sql_get_customer, (customer_id,))
        
        # get customer
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
        
        # return the customer
        return customer_detail

    def get_customer(self, access_token):
        # open and close SQL database connection
        with pyodbc.connect(self.conn_str) as conn:
            # create cursor object
            cursor = conn.cursor()
            
            #print(access_token)

            # get shopper id
            sql_get_shopper_id = "SELECT fk_shopper_id FROM access_token WHERE token = ?"
            cursor.execute(sql_get_shopper_id, (access_token,))

            result = cursor.fetchone()

            if result is not None:
                # get shopper id
                shopper_id = result[0]

                # is shopper_id an integer?
                if isinstance(shopper_id, int):
                    try:
                        customer = self.get_customer_detail(conn, cursor, shopper_id)
                        return jsonify({'message': "Customer profile retrieved successfully", 'data': customer}), 200
                    except Exception as e:
                        error_message = "there is error in getting customer profile" + str(e)
                        return jsonify({'error': error_message}), 500
                else:
                    # customer_id is not valid
                    return jsonify({'error': 'customer_id is not valid'}), 400
            else:
                print("get_customer error")
                return jsonify({'error': "Invalid access token"}), 404



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

                # return access token when successfully added to the database
                return {'message': "access token added successfully", 'data': access_token}, 200

            except Exception as e:
                error_message = "There was an issue in adding access token: " + str(e)
                return {'error': error_message}, 500



    def get_shopper_id(self, email):
        # open and close SQL database connection
        with pyodbc.connect(self.conn_str) as conn:
            # create cursor object
            cursor = conn.cursor()

            # call SP to get shopper ID
            sql_get_id = "EXEC spShopper_GetId ?"
            cursor.execute(sql_get_id, (email,))

            # get result
            result = cursor.fetchone()
            
            # check if result is not None and is an integer
            if result is not None:
                # get shopper id
                shopper_id = result[0]
                
                if isinstance(shopper_id, int):
                    # get the customer detail by shopper id
                    customer_detail = self.get_customer_detail(conn, cursor, shopper_id)
                    # return customer's id
                    return customer_detail['customer_id']
                else:
                    return jsonify({"error": "Shopper ID is not valid"}), 400 
                
            else:
                return jsonify({"error": "Invalid access token or shopper ID not found"}), 404 
    
          
    def get_order_id(self, conn):
        # create cursor object
        cursor = conn.cursor()
        
        
        # get the latest order id by the latest created_date
        sql_get_order_id = "SELECT TOP 1 pk_order_id FROM order_record ORDER BY created_date DESC"
        cursor.execute(sql_get_order_id)
        
        # fetch the row tuple
        result = cursor.fetchone()
        
        
        # get order id
        order_id = result[0]
        
        # is order id an integer? 
        if isinstance(order_id, int):
            return str(order_id)
        else:
            return jsonify({'error': 'Customer\'s id does not exist'}), 404
    
    def add_customer_payment_ui(self, customer_id, order_id, total_price, payment_token, last_4_digits, card_type):
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

                return {'message': 'Payment info is added successfully', 'order_id': order_id}, 200

            except Exception as e:
                error_message = "There was an issue adding payment info: " + str(e)
                return {'error': error_message}, 500

    def get_order_status(self, order_id):
        with pyodbc.connect(self.conn_str) as conn:
            # create cursor object
            cursor = conn.cursor()

            sql_get_status_query = "SELECT order_status FROM order_record WHERE pk_order_id = ?"
            cursor.execute(sql_get_status_query, (order_id,))

            # fetch the row tuple
            result = cursor.fetchone()

            # get order status
            order_status = result[0]

            # is order status a string?
            if isinstance(order_status, str):
                return str(order_status)
            else:
                return jsonify({'error': 'Customer\'s id does not exist'}), 404

    def set_order_status(self, order_status, order_id):
        with pyodbc.connect(self.conn_str) as conn:
            # create cursor object
            cursor = conn.cursor()

            try:
                sql_modify_status = "UPDATE order_record SET order_status = ? WHERE pk_order_id = ?"
                cursor.execute(sql_modify_status, (order_status, order_id))
                conn.commit()

                return {'message': 'Order status is set successfully'}, 200
            except Exception as e:
                error_message = "There was an issue in setting order status: " + str(e)
                return {'error': error_message}, 500

    def set_payment_status(self, payment_status, order_id):
        with pyodbc.connect(self.conn_str) as conn:
            # create cursor object
            cursor = conn.cursor()

            try:
                sql_modify_status = "UPDATE order_record SET payment_status = ? WHERE pk_order_id = ?"
                cursor.execute(sql_modify_status, (payment_status, order_id))
                conn.commit()

                return {'message': 'Payment status is set successfully'}, 200
            except Exception as e:
                error_message = "There was an issue in setting payment status: " + str(e)
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

    def get_payment_ui(self, order_id):
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

    def get_all_orders_ui(self, shopper_id):
        with pyodbc.connect(self.conn_str) as conn:
            # create cursor object
            cursor = conn.cursor()

            if self.is_customer_id_exist(shopper_id, conn):
                try:
                    # get all orders of a customer
                    sql_get_all_orders = "SELECT pk_order_id, created_date, payment_status, total_amount FROM order_record WHERE fk_shopper_id = ?"
                    cursor.execute(sql_get_all_orders, shopper_id)

                    rows = cursor.fetchall()
                    orders = []

                    # iterate through rows of orders
                    for row in rows:
                        order = {
                          'order_id': row.pk_order_id,
                          'order_date': row.created_date,
                          'payment_status': row.payment_status,
                          'order_total': row.total_amount
                        }
                        orders.append(order)
                    conn.commit()

                    # return all orders
                    return jsonify({'message': "All orders displayed successfully", 'data': orders}), 200
                except Exception as e:
                    error_message = "There was an issue displaying orders " + str(e)
                    return jsonify({'error': error_message}), 500
            else:
                return jsonify({'error': "order id does not exist"}), 404

    def get_order_ui(self, order_id):
        with pyodbc.connect(self.conn_str) as conn:
            # create cursor object
            cursor = conn.cursor()

            if (self.is_order_id_exist(order_id, conn)):
                try:
                    # fetch order baded on the given order_id
                    sql_get_order = "SELECT created_date, pk_order_id, subtotal, shipping_fee, total_amount FROM order_record WHERE pk_order_id = ?"
                    cursor.execute(sql_get_order, (order_id,))

                    # get the order
                    data = cursor.fetchone()

                    order_detail = {
                        'order_date': data.created_date,
                        'order_number': data.pk_order_id,
                        'subtotal': data.subtotal,
                        'shipping_fee': data.shipping_fee,
                        'total_amount': data.total_amount
                       }

                    return jsonify({'message': "An order is displayed successfully", 'data': order_detail}), 200
                except Exception as e:
                    error_message = "There was an issue displaying an order " + str(e)
                    return jsonify({'error': error_message}),  500
            else:
                return jsonify({'error': "order_id is not exist"}), 400

    def get_all_order_items_ui(self, order_id):
        with pyodbc.connect(self.conn_str) as conn:
            # create curstor object
            cursor = conn.cursor()

            # if order_id exist
            if (self.is_order_id_exist(order_id, conn)):
                try:
                    # fetch all orders purchased by the customer
                    sql_get_all_orders = """
                    SELECT
                        p.pk_product_id,
                        p.product_category,
                        p.product_name,
                        p.product_price,
                        oi.quantity
                    FROM order_item AS oi
                    JOIN product AS p
                        ON oi.fk_product_id = p.pk_product_id
                    WHERE oi.fk_order_id = ?;
                    """
                    cursor.execute(sql_get_all_orders, (order_id,))

                    # fetch all rows from the cursor
                    rows = cursor.fetchall()

                    # create list to store order items
                    items = []
                    # iterate through rows of order items
                    for row in rows:
                        item = {
                            'product_id': row.pk_product_id,
                            'product_category': row.product_category,
                            'product_name': row.product_name,
                            'product_price': row.product_price,
                            'product_quantity': row.quantity
                        }
                        items.append(item)

                    conn.commit()
                    # return all order items
                    return jsonify({'message': "All order items displayed sucessfully", 'data': items}), 200
                except Exception as e:
                    error_message = "There was an issue displaying all products" + str(e)
                    return jsonify({'error': error_message}), 500

            else:
                return jsonify({'error': "order_id is not exist"}), 400
    
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
                    # get the customer detail by shopper id
                    customer_detail = self.get_customer_detail(conn, cursor, shopper_id)
                    # return customer's first name
                    return customer_detail['first_name']
                else:
                    return jsonify({"error": "Shopper ID is not valid"}), 400

            else:
                print("error here")
                return jsonify({"error": "Invalid access token or shopper ID not found"}), 404

    def validate_order(self, customer_id, orders, conn):
        # check if customer_id exist
        if self.is_customer_id_exist(customer_id, conn) == False:
            return False
        
        # check if all orders exist in the product_table
        for order in orders:
            product_id = order['product_id']
            unit_price = order['unit_price']
            in_stock_quantity = self.get_stock_quantity(product_id, conn)
                            
            if in_stock_quantity is None:
                return False
            
            cursor = conn.cursor()
            
            sql_get_product_id = """
            SELECT 
                pk_product_id 
            FROM product WHERE 
                pk_product_id = ? AND product_price = ? AND in_stock_quantity = ?
            """
            cursor.execute(sql_get_product_id, (product_id, unit_price, in_stock_quantity))
            
            # fetch the row tuple
            product_id_result = cursor.fetchone()
            
            # if product_id does not exist, return False
            if (product_id_result is None):
                return False
        
        # all orders exist
            return True
    
    def get_stock_quantity(self, product_id, conn):
        # create cursor object
        cursor = conn.cursor()
        
        # get in_stock_quantity
        sql_get_stock_query = "SELECT in_stock_quantity FROM product WHERE pk_product_id = ?"
        cursor.execute(sql_get_stock_query, (product_id,))
        
        # fetch row tuple
        stock_result = cursor.fetchone()
        
        # if stock exist, return stock
        if (stock_result is not None and isinstance(stock_result[0], int)):
            return stock_result[0]
        else:
            return None
        
    def validate_quantities(self, orders):
        # loop orders
            for order in orders:
                # get in_stock quantity given product_id
                requested_quantity = order['quantity']
                
                if requested_quantity <= 0:
                    return False
            
            return True
    
    def reserve_stock(self, orders, conn):
        for order in orders:
            product_id = order['product_id']
            requested_quantity = order['quantity']
            
            result, status = self.reserve_stock_quantity(product_id, requested_quantity, conn)
            
            if status != 200:
                return result, status
        return {'message': 'Stock reserved successfully'}, 200
            
    def reserve_stock_quantity(self, product_id, requested_quantity, conn):
        # create cursor object
        cursor = conn.cursor()

        try:
            # Reduce the current stock by the requested quantity, only if 
            # current stock is less than or equal to the current stock.
            sql_update_in_stock_quantity = """
            UPDATE product
            SET in_stock_quantity = in_stock_quantity - ?
            WHERE pk_product_id = ?
                AND ? <= in_stock_quantity
            """
            cursor.execute(sql_update_in_stock_quantity, (requested_quantity, product_id, requested_quantity))
            
            # check whether a product row was actually updated
            if cursor.rowcount == 1:
                    return {'message': 'stocks reduced suceessfully'}, 200
            else:
                return {'error': 'The requested quantity exceeds the available stock'}, 400
        except Exception as e:
            error_message = "There was issue in reducing stocks " + str(e)
            return {'error': error_message}, 500
            
    def calculate_order_total(self, orders):
        # get subtotal
        subtotal = 0
        
        # loop orders
        for order in orders:
            subtotal += order['unit_price'] * order['quantity']
        
        # total ammount
        total_amount = subtotal + self.SHIPPING_COST
        
        # return the calculations
        receipt = {
            'subtotal': subtotal,
            'shipping_fee': self.SHIPPING_COST,
            'total_amount': total_amount
        }
        return receipt
   
    def create_order_record(self, customer_id, orders, receipt, conn):
        # default params
        order_date = datetime.now()
        payment_status = None
        created_date = datetime.now()
        modified_date = None

        # Order statuses: PENDING, PAID
        order_status = "PENDING"

        # create cursor object
        cursor = conn.cursor()

        try:
            sql_customer_id_insert_query = "INSERT INTO order_record VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
            
            cursor.execute(sql_customer_id_insert_query, (customer_id, order_date, receipt['subtotal'], 
            receipt['shipping_fee'], receipt['total_amount'], payment_status, 
            created_date, modified_date, order_status))
            
            # return the order_id of the purchase
            order_id = self.get_order_id(conn)
    
            # add order items to the order_items table and reduce stocks
            result, status = self.create_order_items(order_id, orders, conn)
            
            # success in adding all order items
            if status == 200:
                return result, status
            else:
                # error in adding all order items
                return result, 200

        except Exception as e:
            error_message = "There was an issue adding order record: " + str(e)
            return {'error': error_message}, 500
                
    def create_order_items(self, order_id, orders, conn):
        # default params
        created_date = datetime.now()
        modified_date = None

        # create cursor object
        cursor = conn.cursor()

        # thus, we can add all orders to order item table
        for order in orders:
            try:
                sql_add_order_items = "INSERT INTO order_item VALUES (?, ?, ?, ?, ?, ?)"
                product_id = order['product_id']
                quantity = order['quantity']
                unit_price = order['unit_price']
                cursor.execute(sql_add_order_items, (order_id, product_id, quantity, unit_price, created_date, modified_date))

            except Exception as e:
                error_message = "There was an issue creating order items" + str(e)
                return {'error': error_message}, 500

        # after all orders added and its in_stock_quantity reduced, return a success message
        return {'message': 'All order items is added successfully:', 'order_id': int(order_id)}, 200
                    
    def create_order_ui(self, customer_id, orders):
        # open and close database connection
        with pyodbc.connect(self.conn_str) as conn: 
            try:
                # validate customer and products
                if not self.validate_order(customer_id, orders, conn):
                    # undo changes to the database
                    conn.rollback()
                    
                    return jsonify({'error': ('Either customer ID does not' 
                                    'exist or one or more products are invalid')}), 400
                
                print("validate_order() PASS")
                
                # validate requested quantities
                if not self.validate_quantities(orders):
                    conn.rollback()
                    
                    return jsonify({'error': ('one of the requested quantities is invalid')}), 400
                
                print("validate_quantities() PASS")
                
                # reserve stocks
                result, status = self.reserve_stock(orders, conn)
                
                if status != 200:
                    conn.rollback()
                    return jsonify(result), status
                
                print("reseve_stock() PASS ")
                receipt = self.calculate_order_total(orders)
                
                print(f"calculate order total receipt: {receipt}")
                # create order transaction
                result, status = self.create_order_record(customer_id, orders, receipt, conn)
                
                if status != 200:
                    conn.rollback()
                    
                    return jsonify(result), status
                
                print("create_order_record() PASS")
                
                # everything succeeded
                conn.commit()
                
                order_summary = {
                    'order_id': result['order_id'],
                    'subtotal': receipt['subtotal'],
                    'shipping_fee': receipt['shipping_fee'],
                    'total_amount': receipt['total_amount']
                    }
                
                return jsonify({
                    'message': result['message'],
                    'data': order_summary
                }), 200
                    
            except Exception as e:
                conn.rollback()
                return jsonify({'error': 'The order could not be completed: ' + str(e)}), 500