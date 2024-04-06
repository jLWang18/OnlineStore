import pyodbc
class MyWebService:
    # static  SQL connection
    conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};' 'Server=(localdb)\MSSQLLocalDB;' 'Database=account_receivable;' 'Trusted_Connection=yes;')
    
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
            # self.close_sql(cursor)
            
            return True
        except Exception:
            # close cursor and connection
            self.close_sql(cursor)
            
            return False
    
    # add customer phone
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
                #display err message: email input or phone input is not valid
                return "Customer's email and/or phone is not valid"
    