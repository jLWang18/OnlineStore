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


def contain_phone(phone_number):
    # check if phone number contains digits
    digits = r'[0-9]+'
    
    if (re.search(digits,phone_number)):
        # check if it 10 digits
        if (len(phone_number) == 10):
            return True
        else:
            # phone number is not 10 digits
            return False
            
    else:
        # phone_number is not digits
        return False
    
    
def check_email(email):
    # alphabet
    local = r'[a-zA-Z]|[0-9]'
    # @ symbol
    symbol = r'@'
    # domain
    domain = r'[a-zA-Z0-9]+\.com$'
    
    # comparison is case insensitive
    email = email.lower()
    
    
    # a valid email will contain alphanumeric followed by an @ symbol and the domain name
    if (re.search(local, email) and re.search(symbol, email) and re.search(domain, email)):
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
    # and does not contain any symbols and numbers
    letters = r'[a-zA-z]'
    symbols = r'[@_!#$%^&*()<>{~:]'
    numbers = r'[0-9]'
    
    # check if first name contain symbols
    contain_symbols = re.search(symbols, first_name)
    
    # check if first name contain numbers
    contain_numbers = re.search(numbers, first_name)
    
    # if first name contains only letter and not symbols or numbers
    if ((re.search(letters, first_name)) and (contain_symbols is None) and (contain_numbers is None)):
        # check if valid length
        chars_length = len(first_name)
        if (chars_length >= 3 and chars_length <= 50):
            return True
        else:
            return False
    else:
        return False

def check_last_name(last_name):
    # check if last name contains letters between 3 and 150 letters and 
    # does not contain any symbols and numbers
    letters = r'[a-zA-z]'
    symbols = r'[@_!#$%^&*()<>{~:]'
    numbers = r'[0-9]'
    
    # check if last name contain symbols
    contain_symbols = re.search(symbols, last_name)
    
    # check if last name contain numbers
    contain_numbers = re.search(numbers, last_name)
    
    # if last name contains only letter and not symbols or numbers
    if (re.search(letters, last_name) and (contain_symbols is None) and (contain_numbers is None)):
        # check if valid length
        chars_length = len(last_name)
        if (chars_length >= 3 and chars_length <= 150):
            return True
        else:
            return False
    else:
        return False

def check_password(password):
    # check if password contains at least 8 characters long, 
    # an uppercase, lowercase, a numbers, and a symbol
    uppercase = r'[A-Z]'
    lowercase = r'[a-z]'
    number = r'[0-9]'
    symbol = r'[@_!#$%^&*()<>{~:]'
    
    # get password length
    password_len = len(password)
    
    if (password_len >= 8 and re.search(uppercase, password) and re.search(lowercase, password) 
        and re.search(number, password) and re.search(symbol, password)):
        return True
    else:
        return False 
         

# # define Flask API routes for SwaggerUI to display all customers <--- not needed for now
# @app.route('/api/customer-info/get', methods=['GET'])
# def get_all_customers():
    
#     try:    
#         # instantiate MySwaggerService class
#         swaggerservice = myswaggerservice.MySwaggerService()
        
#         # display customer info by calling the method in MySwaggerService class
#         customer_details = swaggerservice.display_all_customers()
        
#         return jsonify({'message': 'All customer\'s records displayed successfully', 'data': customer_details}), 200
#     except Exception as e:
#         error_message = 'There was an issue displaying customer\'s records' + str(e)
#         return jsonify({'error': error_message}), 400          

@app.route('/api/customer-info/authentication', methods=['GET'])
def get_customer_detail():
     # check the request Content-Type is application/x-www-form-urlencoded
    if request.headers.get('Content-Type', ''):
        return jsonify({'error': 'Unsupported Media Type.  Please send data with Content-Type: application/x-www-form-urlencoded'}), 415
    
    email = request.args.get('email')
    password_string = request.args.get('password')
    
    # convert a string password to bytes
    password = bytes(password_string, 'utf-8')

    # instantiate swagger service
    swaggerservice = myswaggerservice.MySwaggerService()
    # get a customer info
    customer_detail = swaggerservice.display_customer(email,password)

    # if there is a customer, display it
    if(customer_detail is not None):
          return jsonify({'message': 'All Customer\'s records displayed successfully', 'data': customer_detail}), 200
    else:
        return jsonify({'error': 'either email or password is not valid'}), 400

@app.route('/api/customer-info/addCustomer', methods=['POST'])
def add_customer():
    # check the request Content-Type is application/x-www-form-urlencoded
    if request.headers.get('Content-Type', ''):
        return jsonify({'error': 'Unsupported Media Type.  Please send data with Content-Type: application/x-www-form-urlencoded'}), 415

    # get input from query parameteter
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    email = request.args.get('email')
    password_string = request.args.get('password')
    phone_number = request.args.get('phone_number')
    
    
    # first name must be between 3 and 50 letters
    first_name_valid = check_first_name(first_name)
    
    # last name must be between 3 and 150 letters
    last_name_valid = check_last_name(last_name)
    
    # email alphanumeric followed by an @ symbol and the domain name
    email_valid = check_email(email)
    
    # password must contain at least 8 characters long, 
    # an uppercase, lowercase, a numbers, and a symbol
    password_valid = check_password(password_string)
    
    # Check if phone contain only digits
    phone_valid = contain_phone(phone_number)
    
    if (first_name_valid == False):
        error_message = 'Please enter a valid first name at least between 3 and 50 letters'
        return jsonify({'error message': error_message}), 400
    elif(last_name_valid == False):
        error_message = 'Please enter a valid last name at least between 3 and 150 letters'
        return jsonify({'error message': error_message}), 400
    elif(email_valid == False):
         error_message = 'Please enter a valid email at least between 13 and 31 characters'
         return jsonify({'error message': error_message}), 400
    elif(password_valid == False):
        error_message = 'Please enter a valid password at least 8 characters long, 1 uppercase letter, 1 lowercase letter, 1 number, and 1 symbol'
        return jsonify({'error message': error_message}), 400
    elif(phone_valid == False):
         error_message = 'Please enter a valid phone containing 10 digits'
         return jsonify({'error message': error_message}), 400
    else:
        # instatiate swagger service
        swaggerservice = myswaggerservice.MySwaggerService()
        # convert a string password to bytes
        password = bytes(password_string, 'utf-8')
        # add all inputs to the database
        message = swaggerservice.add_customer(first_name, last_name, email, password, phone_number)
        return message

if __name__== "__main__":
    app.run(debug=True)