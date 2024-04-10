from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_swagger_ui import get_swaggerui_blueprint
from datetime import datetime
import pyodbc
import mywebservice
import myswaggerservice
import re
# set up flask application
app = Flask(__name__)



### Swagger specific ###
SWAGGER_URL = '/swagger' 
API_URL = '/static/swagger/swagger.json'

# call factory function to create the Swagger UI blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  
    API_URL,
    config={  
        'app_name': "Online Store API"
    },
)

app.register_blueprint(swaggerui_blueprint, url_prefix = SWAGGER_URL)
### End Swagger specific ###

# define route for rendering the homepage
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# redirect user to the customer info page when the user clicks "sign in"
@app.route('/signin', methods=['GET'])
def signin():
    # redirect to endpoint customer_info
    return redirect(url_for('customer_info_ui'))

# define route for rendering the customer_info page
@app.route("/customer_info", methods=['GET'])
def customer_info_ui():
    return render_template('customer_info.html')

# format phone input
def format_phone(phone):
    # convert phone input in from (XXX)-(XXX)-(XXXX) to XXXXXXXXX format
    replacements = [('(', ''), ('-', ''), (')', '')]
    
    for char, replacement in replacements:
        if char in phone:
            phone = phone.replace(char, replacement)
    
    # make sure there is no spaces         
    phone = phone.replace(' ', '') 
    return phone

# check if phone number contains digits
def contain_digits(phone_number):
    
    # if char is 1, 2, 3,..., or 0, store in num_bucket
    num_bucket = ''
    # if char is alphabet or special chars, store in special_bucket
    special_bucket = ''
    for char in phone_number:
        # store numbers in num_bucket
        if  char == '0':
            num_bucket += char
        elif char == '1':
            num_bucket += char 
        elif char == '2':
            num_bucket += char
        elif char == '3':
            num_bucket += char
        elif char == '4':
            num_bucket += char 
        elif char == '5':
            num_bucket += char
        elif char == '6':
            num_bucket += char
        elif char == '7':
            num_bucket += char 
        elif char == '8':
            num_bucket += char
        elif char == '9':
            num_bucket += char
        else:
            # store in special bucket
            special_bucket += char
            
    # if special_bucket does not contain special chars
    if (special_bucket == ''):
        # check if num_bucket contains only 10 digits
        if (len(num_bucket) == 10):
            return True
        else:
            # num_bucket contains more than 10 digits
            return False
    else:
        # phone_num contains alphabet and/or special chars
        return False
    
def is_valid_email(email):
    # alphabet
    local = r'[a-zA-Z]|[0-9]'
    # numbers
    symbol = r'@'
    # domain
    domain1 = r'[a-zA-Z]|[0-9]'
    domain2 = r'.com'
    
    # comparison is case insensitive
    email = email.lower()
    
    # a valid email will contain alphanumeric followed by an @ symbol and the domain name
    if (re.search(local, email) and re.search(symbol, email) and re.search(domain1, email) and re.search(domain2, email)):
          # a valid email will be between between 13 and 31 chars
          chars_length = len(email)
          if (chars_length >= 13 and chars_length <= 31):
              # email is valid
              return True
          else:
              return False
    else:
        return False
        
def check_first_name(first_name):
    # check if first name contains letters between 3 and 50 chars
    letters = r'[a-zA-z]'
    
    if (re.search(letters, first_name)):
        # check if valid length
        chars_length = len(first_name)
        if (chars_length >= 3 and chars_length <= 50):
            return True
        else:
            return False
    else:
        return False

def check_last_name(last_name):
    # check if last name contains letters between 3 and 150 chars
    letters = r'[a-zA-z]'
    
    if (re.search(letters, last_name)):
        # check if valid length
        chars_length = len(last_name)
        if (chars_length >= 3 and chars_length <= 150):
            return True
        else:
            return False
    else:
        return False

# define Flask API routes for Web UI to add customer to the database
@app.route('/submit_customer', methods=['POST'])
def submit_customer():
        
    # instantiate MyWebService class
    webservice = mywebservice.MyWebService()
    
    # get user input
    first_name = request.form['fname']
    last_name = request.form['lname']
    email = request.form['email']
    phone = request.form['phone-number']
    
    # default params
    created_date = datetime.now()
    modified_date = None
    
    # format phone input
    phone = format_phone(phone)
    
    # call the method from myWebService class 
    message = webservice.add_customer(first_name, last_name, email, phone, created_date, modified_date)
    return message        

       
@app.route('/api/customer-info/<int:customer_id>', methods=['GET'])
def get_customer_detail(customer_id): 
    
    # instantiate swagger service
    swaggerservice = myswaggerservice.MySwaggerService()
    # get a customer info
    customer_detail = swaggerservice.display_customer(customer_id)
    
    # if there is a customer, display it
    if(customer_detail is not None):
          return jsonify({'message': 'All Customer\'s records displayed successfully', 'data': customer_detail}), 200
    else:
        return jsonify({'error': 'Customer ID is not found'})  
         

# define Flask API routes for SwaggerUI to display all customers
@app.route('/api/customer-info/get', methods=['GET'])
def get_all_customers():
    
    try:    
        # instantiate MySwaggerService class
        swaggerservice = myswaggerservice.MySwaggerService()
        
        # display customer info by calling the method in MySwaggerService class
        customer_details = swaggerservice.display_all_customers()
        
        return jsonify({'message': 'All customer\'s records displayed successfully', 'data': customer_details}), 200
    except Exception as e:
        error_message = 'There was an issue displaying customer\'s records' + str(e)
        return jsonify({'error': error_message}), 400          


@app.route('/api/customer-info/addCustomerPhone', methods=['POST'])
def customer_phone():
    
    # Check the request Content-Type is application/x-www-form-urlencoded
    if request.headers.get('Content-Type', ''):
        return jsonify({'error': 'Unsupported Media Type.  Please send data with Content-Type: application/x-www-form-urlencoded'}), 415
    
    # get phone number from query parameter
    phone_number = request.args.get('phone_number')
    
    # check if it is a 10 digits number
    is_number = contain_digits(phone_number)
    
    # if it contains 10 digits number
    if (is_number):
        # add customer to the database by calling swaggerservice
        swaggerservice = myswaggerservice.MySwaggerService()
        message = swaggerservice.add_customer_phone(phone_number)
        return message
    else:
        error_message = 'please enter number containing 10 digits'
        return jsonify({'error': error_message}), 415
  
    
   
@app.route('/api/customer-info/addCustomerEmail', methods=['POST'])
def customer_email():
    # check the request Content-Type is application/x-www-form-urlencoded
    if request.headers.get('Content-Type', ''):
        return jsonify({'error': 'Unsupported Media Type.  Please send data with Content-Type: application/x-www-form-urlencoded'}), 415

    # get email from query parameter
    email = request.args.get('email')
    
    # check if valid email
    is_email = is_valid_email(email)
    
    if (is_email):
        # add email by swagger service
        swaggerservice = myswaggerservice.MySwaggerService()
        message = swaggerservice.add_customer_email(email)
        return message
    else:
        error_message = 'Please enter valid email at least between 13 and 31 characters'
        return jsonify({'error message': error_message}), 415
    
   


@app.route('/api/customer-info/addCustomer', methods=['POST'])
def customer_info():
    
    # check the request Content-Type is application/x-www-form-urlencoded
    if request.headers.get('Content-Type', ''):
        return jsonify({'error': 'Unsupported Media Type.  Please send data with Content-Type: application/x-www-form-urlencoded'}), 415

    # get input from query parameteter
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    email_id = request.args.get('email')
    phone_number_id = request.args.get('phone_number')
    
    # first name must be between 3 and 50 letters
    valid_fn = check_first_name(first_name)
    # last name must be between 3 and 150 letters
    valid_ln = check_last_name(last_name)
    
    if (valid_fn == False):
        error_message = 'Please enter valid first name at least between 3 and 50 characters'
        return jsonify({'error message': error_message}), 415
    elif(valid_ln == False):
        error_message = 'Please enter valid last name at least between 3 and 150 characters'
        return jsonify({'error message': error_message}), 415
    else:
        # if both first name and last_name valid, add them by swagger service
        swaggerservice = myswaggerservice.MySwaggerService()
        message = swaggerservice.add_customer(first_name, last_name, email_id, phone_number_id)
        return message

if __name__== "__main__":
    app.run(debug=True)