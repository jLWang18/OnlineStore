from flask import Flask, jsonify, render_template, request, redirect, url_for, json
import pyodbc
from datetime import datetime
from flask_swagger_ui import get_swaggerui_blueprint

# Import a custom UIService class for API Service call
from webservice import MyWebService

# Set up flask application
app = Flask(__name__)
webservice = MyWebService()

### Swagger specific ###
SWAGGER_URL = '/swagger' 
API_URL = '/static/swagger/swagger.json'

# Call factory function to create the Swagger UI blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  
    API_URL,
    config={  
        'app_name': "Online Store API"
    },
)

app.register_blueprint(swaggerui_blueprint, url_prefix = SWAGGER_URL)
### End Swagger specific ###

# Define route for rendering the homepage
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# redirect user to the customer info page when the user clicks "sign in"
@app.route('/signin', methods=['GET'])
def signin():
    # redirect to endpoint customer_info
    return redirect(url_for('customer_info_ui'))

# Define route for rendering the customer_info page
@app.route("/customer_info", methods=['GET'])
def customer_info_ui():
    return render_template('customer_info.html')

# Format phone input
def format_phone():
    #Convert phone input in from (XXX)-(XXX)-(XXXX) to XXXXXXXXX format
    replacements = [('(', ''), ('-', ''), (')', '')]
    
    for char, replacement in replacements:
        if char in phone:
            phone = phone.replace(char, replacement)
    
    #make sure there is no spaces         
    phone = phone.replace(' ', '') 
    return phone

# Define Flask API routes for customer_info HTML form
@app.route('/submit_customer', methods=['POST'])
def submit_customer():
    # initiates database connection and cursor
    conn = None
    cursor = None
    
    if request.method == 'POST':
        # Establish connection to the database
        conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};' 'Server=(localdb)\MSSQLLocalDB;' 'Database=account_receivable;' 'Trusted_Connection=yes;')
        # Create a cursor object
        cursor = conn.cursor()
        
        #get inputs
        first_name = request.form['fname']
        last_name = request.form['lname']
        email = request.form['email']
        phone = request.form['phone-number']
        
        #default params
        created_date = datetime.now()
        modified_date = None
        
        #format phone input
        phone = format_phone(phone)
        
        #add customer email
        try: 
            #call the method from myWebService class 
            webservice.add_customer_email(conn, cursor, first_name, last_name, email, created_date, modified_date)
        except Exception as e:
            error_message = 'An error occured while adding customer email: ' + str(e)
            return error_message
    else:
        return "Invalid Request"        
         

# Define Flask API routes for SwaggerUI
@app.route('/api/customer-info/get', methods=['GET'])
def get_details():
    # initiates database connection and cursor
    conn = None
    cursor = None
    try:
        #Establish connection to the database
        conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};' 'Server=(localdb)\MSSQLLocalDB;' 'Database=account_receivable;' 'Trusted_Connection=yes;')
        # Create a cursor object
        cursor = conn.cursor()
        sql_get_all_customer_details = "EXEC spCustomerTrial_GetAll"
        cursor.execute(sql_get_all_customer_details)
        
        # Fetch all rows from the cursor
        rows = cursor.fetchall()
        
        # Create a list to store customer details
        customer_details = []
        
        #Iterate through rows of customer details
        for row in rows:
            customer_detail = {
                'customer_id': row.pk_customer_id,   
                'first_name': row.first_name,
                'last_name': row.last_name,
                'email_address': row.email_address,
                'mobile_phone': row.mobile_phone,
                'created_date': row.created_date,
                'modified_date': row.modified_date
            }
            customer_details.append(customer_detail)
        
        conn.commit()
        return jsonify({'message': 'All Customer\'s records displayed successfully', 'data': customer_details}), 200
    
    except Exception as e:
        error_message = 'There was an issue displaying customer\'s records' + str(e)
        return jsonify({'error': error_message}), 400
    
    finally:
        #close cursor and connection
        if cursor:
            cursor.close()
        else:
            conn.close()
        
@app.route('/api/customer-info/<int:customer_id>', methods=['GET'])
def get_customer_detail(customer_id):
    #initiates database connection and cursor
    conn = None
    cursor = None  
    #print("The customer's id arg input is " + str(customer_id))
    try:
        # Check the request Content-Type is application/x-www-form-urlencoded
        if request.headers.get('Content-Type', ''):
            return jsonify({'error': 'Unsupported Media Type.  Please send data with Content-Type: application/x-www-form-urlencoded'}), 415
        
        print("Before gettting the customer_id")
        #Establish connection to the database
        conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};' 'Server=(localdb)\MSSQLLocalDB;' 'Database=account_receivable;' 'Trusted_Connection=yes;')
        # Create a cursor object
        cursor = conn.cursor()
        
    
            
        try: 
            #Execute query
            sql_customer_getbyid = "EXEC spCustomerTrial_GetById ?"
            cursor.execute(sql_customer_getbyid, (customer_id))
            
            #get customer data
            data = cursor.fetchone()
                
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
            return jsonify({'message': 'All Customer\'s records displayed successfully', 'data': customer_detail}), 200
        except Exception:
                error_message = 'Customer ID is not found'
                return jsonify({'error': error_message}), 400
            
    finally:
        # close cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/api/customer-info/addCustomerPhone', methods=['POST'])
def customer_phone():
    
    # initiates database connection and cursor
    conn = None
    cursor = None

    try:
        # Check the request Content-Type is application/x-www-form-urlencoded
        if request.headers.get('Content-Type', ''):
            return jsonify({'error': 'Unsupported Media Type.  Please send data with Content-Type: application/x-www-form-urlencoded'}), 415
        
        # Establish connection to the database
        conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};' 'Server=(localdb)\MSSQLLocalDB;' 'Database=account_receivable;' 'Trusted_Connection=yes;')
        # Create a cursor object
        cursor = conn.cursor()

        # Get phone number from query parameter
        phone_number = request.args.get('phone_number')

        if phone_number is not None:
            # default params
            created_date = datetime.now()
            modified_date = None

            # Insert customer's phone number
            try:
                sql_phone_insert_query = "EXEC spMobilePhoneTrial_InsertAll ?, ?, ?"
                cursor.execute(sql_phone_insert_query, (phone_number, created_date, modified_date))
                conn.commit()
                return jsonify({'message': 'Customer\'s phone number added successfully'}), 200
            except Exception as e:
                error_message = "There was an issue adding customer's phone number: " + str(e)
                return jsonify({'error': error_message}), 500
        else:
            return jsonify({'error': 'phone number parameter is missing'}), 400

    finally:
        # close cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/api/customer-info/addCustomerEmail', methods=['POST'])
def customer_email():

    # initiates database connection and cursor
    conn = None
    cursor = None

    try:
        # Check the request Content-Type is application/x-www-form-urlencoded
        if request.headers.get('Content-Type', ''):
            return jsonify({'error': 'Unsupported Media Type.  Please send data with Content-Type: application/x-www-form-urlencoded'}), 415

        # Establish connection to the database
        conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};' 'Server=(localdb)\MSSQLLocalDB;' 'Database=account_receivable;' 'Trusted_Connection=yes;')
        # Create a cursor object
        cursor = conn.cursor()

        # Get email from query parameter
        email = request.args.get('email')

        if email is not None:
            # default params
            created_date = datetime.now()
            modified_date = None
            
            # Insert customer's email 
            try:
                sql_email_insert_query = "EXEC spEmailAddressTrial_InsertAll ?, ?, ?"
                cursor.execute(sql_email_insert_query, (email, created_date, modified_date))
                conn.commit()
                # return a valid response
                return jsonify({'message': 'Customer\'s email added successfully'}), 200
            except Exception as e:
                error_message = "There was an issue adding customer's email address: " + str(e)
                return jsonify({'error': error_message}), 500
        else:
            return jsonify({'error': 'email parameter is missing'}), 400
        
    finally:
        # close cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@app.route('/customer-info/addCustomer', methods=['POST'])
def customer_info():

    # initiates database connection and cursor
    conn = None
    cursor = None

    try:
        # Check the request Content-Type is application/x-www-form-urlencoded
        if request.headers.get('Content-Type', ''):
            return jsonify({'error': 'Unsupported Media Type.  Please send data with Content-Type: application/x-www-form-urlencoded'}), 415

        
        # Establish connection to the database
        conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};' 'Server=(localdb)\MSSQLLocalDB;' 'Database=account_receivable;' 'Trusted_Connection=yes;')
        # Create a cursor object
        cursor = conn.cursor()

        # Get input from query parameteter
        first_name = request.args.get('first_name')
        last_name = request.args.get('last_name')
        email_id = request.args.get('email')
        phone_number_id = request.args.get('phone_number')

        #get the email from the database
        sql_customer_get_email_byid_query = "EXEC spEmailAddressTrial_GetById ?"
        cursor.execute(sql_customer_get_email_byid_query, (email_id))
        email = cursor.fetchone()

        #get the phone_number from the database
        sql_customer_get_phone_byid_query = "EXEC spPhoneNumberTrial_GetById ?"
        cursor.execute(sql_customer_get_phone_byid_query, (phone_number_id))
        phone = cursor.fetchone()

        #if the email is not found, return jsonify error
        if email is None:
            return jsonify({'error': f'Customer\'s email by email_id {email_id} is not found'}), 400
        elif phone is None:
            return jsonify({'error': f'Customer\'s phone number by phone_number_id {phone_number_id} is not found'}), 400
        
        if first_name and last_name is not None:
            # default params
            created_date = datetime.now()
            modified_date = None
        
            # Insert customer's name
            try:
                sql_customer_insert_query = "EXEC spCustomerTrial_InsertAll ?, ?, ?, ?, ?, ?"
                cursor.execute(sql_customer_insert_query, (first_name, last_name, email_id, phone_number_id, created_date, modified_date))
                conn.commit() 
                return jsonify({'message': 'Customer\'s profile added successfully'}), 200
            except Exception as e:
                error_message = "There was an issue adding customer's info: " + str(e)
                return jsonify({'error': error_message}), 500
        else:
            return jsonify({'error': 'one of the parameter is missing'}), 400
        
    finally:
        # close cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route("/customer-info/get", methods=['GET'])
def get_customer_info():
        try:
            # Establish connection to the database
            conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};' 'Server=(localdb)\MSSQLLocalDB;' 'Database=account_receivable;' 'Trusted_Connection=yes;')
            # Create a cursor object
            cursor = conn.cursor()
            
            # Fetch customers data
            cursor.execute("EXEC spCustomerTrial_GetAll")
            customers = cursor.fetchall()

            # if there are customers data
            if customers:
                # Return the customers as JSON
                return jsonify(customers)
            else:
                return "No customers found", 404
            
        except Exception as e:
            error_message = "There was an issue fetching customer data: " + str(e)
            return error_message
        
        finally:
        # close cursor and connection
            cursor.close()
            conn.close()

if __name__== "__main__":
    app.run(debug=True)