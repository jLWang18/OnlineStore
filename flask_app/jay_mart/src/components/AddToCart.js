import { useNavigate } from 'react-router-dom';
import  useCart  from '../hooks/useCart.js';
import '../styles/styles.css';
import useCheckout from '../hooks/useCheckout.js';
import { useEffect } from 'react';

const SHIPPING_COST = 5

export default function AddToCart() {
    const navigate = useNavigate();

    const { selectedItems } = useCart();

    
    const {subtotal, setSubtotal, shippingFee, setShippingFee, totalAmount, setTotalAmount} = useCheckout();

    useEffect(() => {
        // calculate subtotal (without shipping cost) and totalAmount (with shipping cost) 
        const itemsTotalPrice = (selectedItems) => {
            // loop thrrough selectedItems array and calculate total prices
            let subtotal = 0;
            for (let i = 0; i < selectedItems.length; i++) {
                // subtotal amount of an item = price * quantity
                subtotal += selectedItems[i].product_price * selectedItems[i].in_stock_quantity;

            }
             // total price of an item = subtotal + shipping cost
            let totalAmount = subtotal + SHIPPING_COST;

            setSubtotal(subtotal)
            setShippingFee(SHIPPING_COST)
            setTotalAmount(totalAmount)
        }

        itemsTotalPrice(selectedItems);

    }, [selectedItems, setSubtotal, setTotalAmount])
      

    return (
        <>
        <div class="display-container">
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
        
        <label><h4>items ({selectedItems.length}): ${subtotal}</h4></label>
        <label><h4>shipping: ${shippingFee}</h4></label>
        <label><h4>subtotal: ${totalAmount}</h4></label>

        <div class="options">
            <button class="button" onClick={() => navigate("/payment")}>Proceed to Payment</button>
            <button class="button" onClick={() => navigate("/")}>Cancel</button>
        </div>
        </div>
      </>
    );
}