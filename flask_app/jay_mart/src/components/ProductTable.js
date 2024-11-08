import { useEffect } from 'react';
import { displayTable } from '../logic/display_products.js';
import { useNavigate } from 'react-router-dom';

const ProductTable = () => {
  const navigate = useNavigate();

    // display products table
     useEffect(() => {
       displayTable()
     }, [])
     
     return (
       <>
       <table id="product-table">
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
         <tbody id="data-output">
         </tbody>
       </table>
       <button type="submit" onClick={() => navigate("/addtocart")}>Add to Cart</button>
       </>
     )
 
 }

 export default ProductTable