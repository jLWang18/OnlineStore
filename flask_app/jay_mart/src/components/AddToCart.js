import { useNavigate } from 'react-router-dom';
import  useCart  from '../hooks/useCart.js';
import '../styles/styles.css';
import useCheckout from '../hooks/useCheckout.js';
import { useEffect } from 'react';
import { addOrderRecord } from '../logic/add_order_record.js';
import { addOrderItem } from '../logic/add_order_item.js';
import useCustomer from '../hooks/useCustomer.js';

const SHIPPING_COST = 5

export default function AddToCart() {
    const navigate = useNavigate();

    const {selectedItems} = useCart();

    
    const {subtotal, setSubtotal, shippingFee, setShippingFee, totalAmount, setTotalAmount} = useCheckout();

    const {customerId} = useCustomer();

    const addOrder = async () => {
        // add customer's id, subtotal, shippingFee, and total price to the order_record table
        const orderId = await addOrderRecord(customerId, subtotal, shippingFee, totalAmount)
        
        // loop over selectedItem
        for (let i = 0; i < selectedItems.length; i++) {
            // add each selected product to the order_item table
            const product_id = selectedItems[i].product_id
            const unit_price = selectedItems[i].product_price
            const quantity = selectedItems[i].in_stock_quantity
        
            await addOrderItem(orderId, product_id, unit_price, quantity)
        }

        // navigate to payment page
        navigate(`/payment/${orderId}`)

        
    }

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

    }, [selectedItems, setSubtotal, setShippingFee, setTotalAmount])
      

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
            <button class="button" onClick={() => addOrder()}>Proceed to Payment</button>
            <button class="button" onClick={() => navigate("/")}>Cancel</button>
        </div>
        </div>
      </>
    );
}