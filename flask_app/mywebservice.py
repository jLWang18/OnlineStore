import pyodbc
import os
class MyWebService:
  # accessing environment variables for SQL DB connection 
  conn_str = os.environ.get('DB_CONNECTION')
  
  # display products
  def show_products_ui(self):
       # open and close SQL database connection
        with pyodbc.connect(self.conn_str) as conn:
            # create cursor object
            cursor = conn.cursor()
            
            # call SP to retrieve data
            sql_get_all_products = "EXEC spProduct_GetAll"
        
            cursor.execute(sql_get_all_products)
            
            # Fetch all rows from the cursor
            rows = cursor.fetchall()
            
            # Create a list to store products
            products = []
            
            # Iterate through rows of products
            for row in rows:
                product = {
                    'product_id': row.pk_product_id,   
                    'product_category': row.product_category,
                    'product_name': row.product_name,
                    'product_price': row.product_price,
                    'in_stock_quantity': row.in_stock_quantity,
                    'created_date': row.created_date,
                    'modified_date': row.modified_date
                    }
                products.append(product)
            
            conn.commit()
            
        # diplay products    
        return products
    