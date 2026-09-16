# OnlineStore Project Milestones

## M1: Customer Registration, Login, and Orders ✅

1. **Add customers to the website**
   - Require basic customer information:
     - First name
     - Last name
     - Email
     - Phone number

2. **Enable customers to log in to the website**
   - Allow customers to log in using their email and password.
   - Securely save customer passwords using password hashing and salting with the bcrypt algorithm.

3. **Enable customers to place orders**
   - Add a custom American Foods table.
   - Allow customers to submit orders.
   - Associate each customer's order with their customer record in the database.
   - Add orders through the Flask API and Swagger UI.
   - Add orders through the website.

4. **Launch the website**

---

## M2: Product Selection and Order History ✅

1. **Select multiple products with a specified quantity**
   - Allow customers to select multiple American Foods products.
   - Allow customers to specify the quantity for each product.

2. **View confirmed orders**

---

## M3: Payment Information and Order History ✅

1. **Enable customers to enter transaction information**
   - Name on card
   - Credit card number
   - Card type
   - Expiration date
   - Verification code

2. **View order history**
   - Allow customers to click on their profile.
   - Display their order history.

---

## M4: Product UI and Error Handling

1. **Improve the Product Table layout**
   - Use CSS Grid or Flexbox to improve the product display and layout.

2. **Create a Product Detail page**
   - Allow users to click on a product to view its details.
   - Add an **Add to Cart** button on the Product Detail page.

3. **Improve duplicate email validation**
   - Highlight the email address input field when a customer tries to register with an email address that is already in use.

4. **Improve backend error handling**
   - Update the backend to return JSON-formatted error messages.
   - Allow React to display the backend error message directly without rewriting or customizing the message on the frontend.

## M5: Shipping Information and Saved Customer Information

1. **Enable customers to enter their shipping address**
   - Street Address 1
   - Street Address 2
   - City
   - State
   - ZIP code

2. **Save payment methods**
   - Save customers' payment method information for future transactions.

3. **Save shipping addresses**
   - Save customers' shipping address information for future transactions.

