import { useState, useEffect } from 'react';
import { getProductList } from '../logic/display_products';
import { useNavigate } from 'react-router-dom';
import  useCart  from '../hooks/useCart'
import '../styles/styles.css';

const ProductTable = () => {
  const navigate = useNavigate();

  const {selectedItems, onItemSelect} = useCart();
  const [products, setProducts] = useState([]);



    // fetch products when component mounts
     useEffect(() => {
       const fetchData = async () => {
        // fetch products
        const data = await getProductList();
        // set state with fetched products
        setProducts(data);
       };
       // set state with fetched products
      fetchData();
     }, [])

     const unSelectItems = () => {
      // loop through selected items
      selectedItems.forEach(item => {
        // for each item in eselected items, deselect item
        onItemSelect(item)
        
      });
     }
     
     return (
       <>
      <table class="display-table" id="product-table">
        <thead>
          <tr>
              <th>Select</th>
              <th>Product ID</th>
              <th>Product Category</th>
              <th>Product Name</th>
              <th>Price</th>
              <th>Quantity</th>
          </tr>
        </thead>
        <tbody>
            {products.map((product) => {
              const isChecked = selectedItems.some((item) => item.product_id === product.product_id)
              return (
                <tr key={product.product_id}>
                  <td>
                    <input 
                      type="checkbox"
                      checked= {isChecked}
                      onChange={() => onItemSelect(product)} />
                  </td>
                  <td>{product.product_id}</td>
                  <td>{product.product_category}</td>
                  <td>{product.product_name}</td>
                  <td>{product.product_price}</td>
                  <td>{product.in_stock_quantity}</td>
                </tr>
              )
            })}
        </tbody>
      </table>
        
        {/* Navigte to addToCart page upon clicking*/}
       <div class="options">
            <button class="button" type="button" onClick={() => navigate("/addtocart")}>Add to Cart</button>
            <button class="button" type="reset" onClick={unSelectItems}> Unselect all</button>
       </div>
       </>
     )
 
 }

 export default ProductTable