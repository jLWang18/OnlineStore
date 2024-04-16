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


def contain_digits(phone_number):
    # check if phone number contains digits
    digits = r'[0-9]'
    
    if (re.search(digits,phone_number)):
        return True
    else:
        return False
    
    
def is_valid_email(email):
    # alphabet
    local = r'[a-zA-Z]|[0-9]'
    # @ symbol
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

def passwordValidation(password):
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
        

# define Flask API route for Web UI to add customer to the database
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

# define Flask API route for Swagger UI to add customer's password to the database
@app.route('/api/customer-info/addPassword', methods=['POST'])
def add_password():
       # check the request Content-Type is application/x-www-form-urlencoded
    if request.headers.get('Content-Type', ''):
        return jsonify({'error': 'Unsupported Media Type.  Please send data with Content-Type: application/x-www-form-urlencoded'}), 415

    # get input from query parameteter in bytes form
    password_string = request.args.get('password')
    
    # check if password contains at least 8 characters long, 
    # an uppercase, lowercase, a numbers, and a symbol
    password_valid = passwordValidation(password_string)
    
    if (password_valid):
        # instantiate swaggerservice
        swaggerservice = myswaggerservice.MySwaggerService()
        # convert a string password to bytes
        password = bytes(password_string, 'utf-8')
        # add to the database
        message = swaggerservice.add_shopper_password(password)
        return message
    else:
        error_message = 'Please enter password at least 8 characters long, 1 uppercase letter, 1 lowercase letter, 1 number, and 1 symbol'
        return jsonify({'error message': error_message}), 415
    
    
# define Flask API route for Swagger UI to add customer to the database
@app.route('/api/customer-info/addCustomer', methods=['POST'])
def add_customer():
    # check the request Content-Type is application/x-www-form-urlencoded
    if request.headers.get('Content-Type', ''):
        return jsonify({'error': 'Unsupported Media Type.  Please send data with Content-Type: application/x-www-form-urlencoded'}), 415

    # get input from query parameteter
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    email = request.args.get('email')
    password_id = request.args.get('password')
    phone_number = request.args.get('phone_number')
    
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
        message = swaggerservice.add_customer(first_name, last_name, email, password_id, phone_number)
        return message

if __name__== "__main__":
    app.run(debug=True)