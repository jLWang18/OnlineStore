import { useNavigate } from 'react-router-dom';
import  useCart  from '../hooks/useCart.js';
import '../styles/styles.css';

const SHIPPING_COST = 5

export default function AddToCart() {
    const navigate = useNavigate();

    const { selectedItems } = useCart();

    const itemsTotalPrice = () => {
        // loop thrrough selectedItems array and calculate total prices
        let totalPrice = 0;
        for (let i = 0; i < selectedItems.length; i++) {
            // total price of an item = price * quantity
            totalPrice += selectedItems[i].product_price * selectedItems[i].in_stock_quantity;

        }
        return totalPrice;
    }

    const itemsSubtotal = () => {
        let totalPrice = itemsTotalPrice();
        
        return totalPrice + SHIPPING_COST;
    }

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
        
        <label><h4>items ({selectedItems.length}): ${itemsTotalPrice()}</h4></label>
        <label><h4>shipping: ${SHIPPING_COST}</h4></label>
        <label><h4>subtotal: ${itemsSubtotal()}</h4></label>

        <div class="options">
            <button class="button" onClick={() => navigate("/payment")}>Proceed to Payment</button>
            <button class="button" onClick={() => navigate("/")}>Cancel</button>
        </div>
        </div>
      </>
    );
}