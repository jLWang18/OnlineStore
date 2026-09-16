# Online Store Website

## Overview

The Online Store Website is an e-commerce platform that enables customers to make purchases using a credit-based system. This project demonstrates full-stack development expertise in SQL, Python (Flask API), and React, along with business transaction logic.

## Features

* **User Authentication** – Secure login and account management.

* **Product Catalog** – Browse available products with detailed information.

* **Shopping Cart** – Add, view, and remove products.

* **Product Quantity Selection** – Select the quantity of each food item to purchase.

* **Order Management** – Place orders and view confirmed and past orders.

* **Payment Information** – Enter transaction information when placing an order.

* **Customer Profile** – View order history through the customer profile.

## Recent Updates
#### AddToCart Feature
* Customer can add products to their cart after logging in or signing up.

* Customers can view their selected products in the cart.

* Customers can remove selected products from the cart.

* Customers can select the quantity of each food item they want to purchase.

* The quantity selection is limited to the available stock.

* Products with zero stock are displayed as Out of Stock.

#### Demo Videos
* Demo Video 1: [Returning Customer: Shopping and Selecting Quantity](https://www.loom.com/share/38222d79072a456a8ec8780c6b7b124f)

* Demo Video 2: [New Customer: Sign Up, Shopping, and Selecting Quantity](https://www.loom.com/share/9891dec5ecdc4468bfd3dabf3a777e40)

## Prerequisites
Before running the website, do the following:

* Intall Visual Studio Code 1.87.2
* Install SQL Server Management Studio 19.1
* Clone the project
* Install requirements.txt
* Start Flask API:
    * Install virtual environment (virtualenv) →  ```pip install virtualenv```
    * Create a virtual environment in your project → ```virtualenv venv```
    * Activate virtual environment →  ```venv\Scripts\activate```

## Running the Website
To run the website:
1. Run app.py via python app.py
2. To stop running the website, press ```CTRL + C``` and exit virtual environment via ```deactivate``` 

## Deployment
For simplicity, this app does not include HTTPS, so it's strongly recommended to deploy behind a HTTPS reverse proxy (e.g. nginx or managed cloud load balancer)

