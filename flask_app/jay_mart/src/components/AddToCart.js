import { useNavigate } from 'react-router-dom';
import  useCart  from '../hooks/useCart.js';

export default function AddToCart() {
    const navigate = useNavigate();

    const { selectedItems } = useCart();

    return (
        <>
        <h1>Your Cart Items</h1>
        <table id="cart-table">
         <thead>
           <tr>
               <th>Product ID</th>
               <th>Product Category</th>
               <th>Product Name</th>
               <th>Price</th>
               <th>Quantity</th>
           </tr>
         </thead>
         <tbody>
            {selectedItems.map((selectedItem) => {
                return (
                    <tr key={selectedItem.product_id}>
                        <td>{selectedItem.product_id}</td>
                        <td>{selectedItem.product_category}</td>
                        <td>{selectedItem.product_name}</td>
                        <td>{selectedItem.product_price}</td>
                        <td>{selectedItem.in_stock_quantity}</td>
                    </tr>
                )
            })}
         </tbody>
       </table>
        <button onClick={() => navigate("/payment")}>Proceed to Payment</button>
        <button onClick={() => navigate("/")}>Cancel</button>
        </>
    );
}