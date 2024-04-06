from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_swagger_ui import get_swaggerui_blueprint
from datetime import datetime
import pyodbc
import mywebservice
import myswaggerservice

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


@app.route('/api/customer-info/addCustomerPhone', methods=['POST'])
def customer_phone():
    
    # Check the request Content-Type is application/x-www-form-urlencoded
    if request.headers.get('Content-Type', ''):
        return jsonify({'error': 'Unsupported Media Type.  Please send data with Content-Type: application/x-www-form-urlencoded'}), 415
    
    # get phone number from query parameter
    phone_number = request.args.get('phone_number')  
    
    # instantiate swagger service 
    swaggerservice = myswaggerservice.MySwaggerService()
    
    message = swaggerservice.add_customer_phone(phone_number)
    
    return message
   
@app.route('/api/customer-info/addCustomerEmail', methods=['POST'])
def customer_email():
    # check the request Content-Type is application/x-www-form-urlencoded
    if request.headers.get('Content-Type', ''):
        return jsonify({'error': 'Unsupported Media Type.  Please send data with Content-Type: application/x-www-form-urlencoded'}), 415

    # get email from query parameter
    email = request.args.get('email')
    
    # instantiate swagger service
    swaggerservice = myswaggerservice.MySwaggerService()
    
    # add email
    message = swaggerservice.add_customer_email(email)

    return message

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
    
    # instantiate swaggerservice
    swaggerservice = myswaggerservice.MySwaggerService()
    
    # add customer
    message = swaggerservice.add_customer(first_name, last_name, email_id, phone_number_id)
    
    return message

if __name__== "__main__":
    app.run(debug=True)