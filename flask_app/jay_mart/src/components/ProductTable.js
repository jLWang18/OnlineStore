import { useEffect} from 'react';
import { displayTable, handleOrder } from '../logic/display_products.js';

const ProductTable = () => {
    // display products table
     useEffect(() => {
       displayTable()
     }, [])
     
     return (
       <>
       <table id="myTable">
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
       <button type="submit" onClick={handleOrder}>Add to Cart</button>
       </>
     )
 
 }

 export default ProductTable