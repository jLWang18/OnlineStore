import { useEffect } from "react";
import { useNavigate } from 'react-router-dom';
import { displayCart } from "../logic/display_products";

export default function AddToCart() {
    const navigate = useNavigate();

    useEffect(() => {
        // display user's selected items
        displayCart()
    }, [])

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
         <tbody id="data-output">
         </tbody>
       </table>
        <button onClick={() => navigate("/payment")}>Proceed to Payment</button>
        <button onClick={() => navigate("/")}>Cancel</button>
        </>
    );
}