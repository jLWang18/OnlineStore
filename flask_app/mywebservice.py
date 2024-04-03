class MyWebService:
    
    #add customer email
    def add_customer_email(conn, cursor, email, created_date, modified_date):
        try:
          #First add email to the email table
            sql_email_insert_ui_query = "EXEC spEmailAddressTrial_InsertAll ?, ?, ?"
            cursor.execute(sql_email_insert_ui_query, (email, created_date, modified_date))
            conn.commit()
            return True
        except Exception as e:
            return False
    
    #add customer phone
    def add_customer_phone(conn, cursor, phone, created_date, modified_date):
        try:
            #second add phone to the phone table
            sql_phone_insert_ui_query = "EXEC spMobilePhoneTrial_InsertAll ?, ?, ?"
            cursor.execute(sql_phone_insert_ui_query, (phone, created_date, modified_date))
            conn.commit()
            return True
        except Exception as e:
            return False
    
    #get email id from the database
    def get_email_id(conn, cursor, email):
        email_id = None
        sql_customer_get_email_byid_query = "EXEC spEmailAddressTrial_GetIdByEmail ?"
        cursor.execute(sql_customer_get_email_byid_query, (email))
        
        #fetch the row tuple
        result = cursor.fetchone()
        
        #check if result is not None and is an integer
        if result is not None and isinstance(result[0], int):
            #assigned the first tuple value to email id
            email_id = result[0]
            return email_id
        else:
            print("Error: email_id is not an integer or is None")
    
    #get phone id from the database
    def get_phone_id(conn, cursor, phone):
        sql_customer_get_phone_byid_query = "EXEC spMobilePhoneTrial_GetIdByPhone ?"
        cursor.execute(sql_customer_get_phone_byid_query, (phone))
        
        #fetch the row tuple
        result = cursor.fetchone()
        
        #check if result is not None and is an integer
        if result is not None and isinstance(result[0], int):
            #assigned the first tuple value to phone id
            phone_id = result[0]
            return phone_id
        else:
            print("Error: phone_id is not an integer or None")
            
    #submit customer info logic
    def add_customer(conn, cursor, first_name, last_name, email, phone, created_date, modified_date):
        
        # add customer email to the database and check if added successfully
        is_email_valid = add_customer_email(conn, cursor, email, created_date, modified_date)
          
        # add customer phone to the database and check if added successfully
        is_phone_valid = add_customer_phone(conn, cursor, phone, created_date, modified_date)
            
        #get the email id from the database
        email_id = get_email_id(conn, cursor, email)
        
        #get the phone_id from the database
        phone_id = get_phone_id(conn, cursor, phone)
        
        #add first name, last name, email, and phone to the database 
        if is_email_valid and is_phone_valid:
            try:
                sql_customer_insert_ui_query = "EXEC spCustomerTrial_InsertAll ?, ?, ?, ?, ?, ?"
                cursor.execute(sql_customer_insert_ui_query, (first_name, last_name, email_id, phone_id, created_date, modified_date))
                conn.commit()
                #display UI sucess message
                return "Success: customer added successfully"
            except Exception as e:
                # display UI error message
                error_message = "There is an error in adding customer: " + str(e)
                return error_message
        else:
                #display err message: email input or phone input is not valid
                return "Customer's email and/or phone is not valid"
    