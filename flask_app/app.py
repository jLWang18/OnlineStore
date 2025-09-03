from flask import Flask, jsonify, render_template, request, redirect, url_for, session, make_response
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, create_refresh_token, set_access_cookies
from flask_swagger_ui import get_swaggerui_blueprint
from datetime import datetime, timedelta
from flask_cors import CORS
import pyodbc
import uuid
import mywebservice
import myswaggerservice
import re, os
import json



# set up flask application
app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = True # set to True for HTTPS only
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(seconds=10)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(hours=1)


# set up JWT token
jwt = JWTManager(app)


# enable CORS so that any local host port (in this case, React application)
# can request for resources from this Flask server
cors = CORS(app, resources={
    r"/api/products": {
        "origins": ["http://localhost:3000"]
   }
    ,
    r"/api/login": {
        "origins": ["http://localhost:3000"]
    },
     r"/api/signup": {
        "origins": ["http://localhost:3000"]
    },
    r"/api/whoami": {
        "origins": ["http://localhost:3000"],
    },
    r"/api/getProfile": {
        "origins": ["http://localhost:3000"]
    },
    r"/api/addOrderRecord": {
        "origins": ["http://localhost:3000"]
    },
    r"/api/addOrderItem": {
        "origins": ["http://localhost:3000"]
    }
    
}, supports_credentials= True)

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

# check if phone number contains digits
def contain_phone(phone_number):
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
    
# check if email is in correct format    
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

# check if first name contains letters between 3 and 50 chars
# and does not contain any symbols and numbers        
def check_first_name(first_name):
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

# check if last name contains letters between 3 and 150 letters and 
# does not contain any symbols and numbers
def check_last_name(last_name): 
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

# check if password contains at least 8 characters long, 
# an uppercase, lowercase, a numbers, and a symbol
def check_password(password):    
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

# define Flask API route for React UI to get products in the homepage
@app.route('/api/products', methods=['GET'])
def get_products():
    # instantiate web service
    webrservice = mywebservice.MyWebService()
    
    # get products
    products = webrservice.get_products()
    return products

# define Flask API route for React UI to get customer
@app.route('/api/getProfile', methods=['GET'])
def get_profile():
    # get the access token
    data = request.headers.get("Authorization")
    
    if not data:
        return jsonify({'error': "Authorization token is missing"}), 401
    
    try:
        # extract token part if prefixed with "Bearer"
        if data.startswith("Bearer "):
            data = data.split(" ")[1]
            parsed_data = json.loads(data)
            access_token = parsed_data["accessToken"] 
        else:
            return jsonify({"error": "Invalid Authorization format"}), 401
        
        # instatiate web service
        webservice = mywebservice.MyWebService()
        
        # get customer
        response = webservice.get_customer(access_token)
    
        # return customer data
        return response
    except Exception as e:
        return jsonify({"error": "Unexpected server error: " + str(e)}), 500

# define Flask API route for React UI to add customer's order
@app.route('/api/addOrderRecord', methods=['POST'])
def addOrder_ui():
    # get input from payment form
    data = request.get_json()
    customer_id = data["customer_id"]
    subtotal = data["subtotal"]
    shipping_fee = data["shipping_fee"]
    total_amount = data["total_amount"]
    
    # instatiate web service
    webservice = mywebservice.MyWebService()
    
    # return the order id of the purchase
    response = webservice.add_customer_order(customer_id, subtotal, shipping_fee, total_amount)
    return response

# define Flask API route for React UI to add customer's order item
@app.route("/api/addOrderItem", methods=['POST'])
def addOrderItem_ui():
    # get input from input parameter
    data = request.get_json()
    order_id = data["order_id"]
    product_id = data["product_id"]
    unit_price = data["unit_price"]
    quantity = data["quantity"]
    
    # instatiate web service
    webservice = mywebservice.MyWebService()
    
    message = webservice.add_customer_order_item(order_id, product_id, unit_price, quantity)
    return message
    
 
# define Flask API route for React UI to authenticate a customer
@app.route('/api/login', methods=['POST'])
def login():
    # get input from login form
    data = request.get_json()
    email = data["email"]
    password_string = data["password"]
    
    # instatiate web service
    webservice = mywebservice.MyWebService()
    # convert a string password to bytes
    password = bytes(password_string, 'utf-8')
    
    # check if email and password are valid  
    is_authentication_valid =  webservice.authenticate_customer_ui(email, password)
    
    if (is_authentication_valid):
        
        # create access token with user's email as identity
        access_token = create_access_token(identity=email)
        
        # get shopper id
        shopper_id = webservice.get_shopper_id(email)
        
        if (shopper_id is None):
            return jsonify({"error: there is an issue in getting shopper id"}, 500)
        
        # store access token in the database
        webservice.add_token(shopper_id, access_token)
        
        return jsonify({"accessToken": access_token}), 200
    else:
        return jsonify({'error': "Unauthorized"}), 401

# define Flask API route for React UI to add new customer to the database    
@app.route('/api/signup', methods=["POST"])
def signup():
    # get input from signup form
    data = request.get_json()
    first_name = data["first_name"]
    last_name = data["last_name"]
    email = data["email"]
    password_string = data["password"]
    phone_number = data["phone_number"]
    
    
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
        webservice = mywebservice.MyWebService()
        # convert a string password to bytes
        password = bytes(password_string, 'utf-8')
        # add all inputs to the database
        message = webservice.add_customer(first_name, last_name, email, password, phone_number)
        return message
    
@app.route('/api/whoami', methods=["GET"])
def whoami():
    # get the access token
    data = request.headers.get("Authorization")
    
    
    if not data:
        return jsonify({'error': "Authorization token is missing"}), 401
    
    # extract token part if prefixed with "Bearer"
    if data.startswith("Bearer "):
        data = data.split(" ")[1]
        parsed_data = json.loads(data)
        access_token = parsed_data["accessToken"] 
     
    # instatiate web service
    webservice = mywebservice.MyWebService()
     
    # get customer's first name
    response = webservice.get_customer_name(access_token)
    
    # return customer data
    return response

# define Flask API routes for SwaggerUI to display products after user is authenticated and verified
@app.route('/api/customer-info/getProducts', methods=['GET'])
def get_all_customers():
    email = request.args.get('email')
    password_string = request.args.get('password')
    
    # convert a string password to bytes
    password = bytes(password_string, 'utf-8')

    # instantiate swagger service
    swaggerservice = myswaggerservice.MySwaggerService()
    
    # get all products
    message = swaggerservice.display_products(email,password)
    
    return message   

# define Flask API routes for SwaggerUI to display customer's profile after user is authenticated and verified
@app.route('/api/customer-info/getProfile', methods=['GET'])
def get_customer_detail():   
    customer_id = request.args.get('customer_id')

    # instantiate swagger service
    swaggerservice = myswaggerservice.MySwaggerService()
    
    # display customer profile
    message = swaggerservice.display_customer(customer_id)

    return message

# define Flask API routes for SwaggerUI to add a customer to the database
@app.route('/api/customer-info/addCustomer', methods=['POST'])
def add_customer():
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
    
# define Flask API routes for SwaggerUI to authenticate a customer
@app.route('/api/customer-info/authentication', methods=['POST'])
def authenticate():
    # get email & password input
    email = request.args.get("email")
    password_string = request.args.get("password")
    
     # email alphanumeric followed by an @ symbol and the domain name
    email_valid = check_email(email)
    
    # password must contain at least 8 characters long, 
    # an uppercase, lowercase, a numbers, and a symbol
    password_valid = check_password(password_string)
    
    if(email_valid == False):
         error_message = 'Please enter a valid email at least between 13 and 31 characters'
         return jsonify({'error message': error_message}), 400
    elif(password_valid == False):
        error_message = 'Please enter a valid password at least 8 characters long, 1 uppercase letter, 1 lowercase letter, 1 number, and 1 symbol'
        return jsonify({'error message': error_message}), 400
    else:
        # instatiate swagger service
        swaggerservice = myswaggerservice.MySwaggerService()
        # convert a string password to bytes
        password = bytes(password_string, 'utf-8')
        # check if email and password exist
        message = swaggerservice.authenticate_customer(email, password)
        return message

# define Flask API routes for SwaggerUI to add customer's order
@app.route("/api/customer-info/addOrderRecord", methods=['POST'])
def addOrder():
    # get input parameters
    customer_id = request.args.get("customer_id")
    subtotal = request.args.get("subtotal")
    shipping_fee = request.args.get("shipping_fee")
    total_amount = request.args.get("total_amount")
    
    # instatiate swagger service
    swaggerservice = myswaggerservice.MySwaggerService()
    
    message = swaggerservice.add_customer_order(customer_id, subtotal, shipping_fee, total_amount)
    return message

# define Flask API routes for SwaggerUI to add customer's order item
@app.route("/api/customer-info/addOrderItem", methods=['POST'])
def addOrderItem():
    # get input from query parameteter
    order_id = request.args.get("order_id")
    product_id = request.args.get("product_id")
    unit_price = request.args.get("unit_price")
    quantity = request.args.get("quantity")
    
    # instatiate swagger service
    swaggerservice = myswaggerservice.MySwaggerService()
    
    message = swaggerservice.add_customer_order_item(order_id, product_id, unit_price, quantity)
    return message


# start the Flask application if this script is executed directly
if __name__== "__main__":
    app.run(debug=True)