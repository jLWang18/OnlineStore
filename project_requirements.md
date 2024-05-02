# Online Store Project Requirements
### Purpose
Develop an e-commerce platform tailored for selling and purchasing diverse products (e.g., clothes, shoes, foods, electronics, etc.).

**Development Tools:** Microsoft SQL Server Database, Python, Flask API, React

### Key Features

**User Interface Development:**
-   Enable customers to log in as registered users or shop as guests, requiring basic information such as first name, last name, email address, phone number, and password for registration.
-   Facilitate browsing of products within the platform.
-   Allow customers to place multiple orders, both immediate purchases and wishlist items.
    
  **Transaction Management:**
-   Capture and save transaction details, including shipping and billing addresses (with the option to use the same address) and credit card information (Name on card, Credit Card Number, Card Type, Expiration Date, Verification Code).
-   Provide a seamless order submission process.
-   Notify customers promptly regarding confirmed orders and estimated delivery times.
    
**Credit Purchase System (Accounts Receivable):**
-   Implement a mechanism enabling customers to make purchases on credit.
-   Establish a fixed credit limit per customer, necessitating settlement of outstanding balances exceeding this limit before further credit transactions occur.
-   Maintain records of credit sales, current assets owed by customers, and credit limits.
    
**Supplier Management:**
-   Facilitate order placement with suppliers to replenish product stocks,
-   Keep track of fast-moving products (high-demand, quick-selling items) and slow-moving products (low-demand, niche, or seasonal items)
-   Enable credit purchases from suppliers as necessary (Account Payable).
    
**Inventory and Financial Tracking:**
-   Monitor inventory levels and initiate restocking procedures as needed.
-   Keep records of operational costs associated with accounts receivable:
  	- Generated from sales and services provided to customers.
-   Keep records of operational costs associated with accounts payable:
    - Expenses such as purchasing inventory, raw materials, equipment, and services from suppliers.
-   Calculate profit and loss margins by subtracting the operational cost of accounts payable from the operational cost of accounts receivable ( PL = operational cost of AR - operational cost of AP).
-   Track current assets, current liabilities, debit, credit, and potential bad debt.