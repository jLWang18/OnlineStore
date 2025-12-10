import { useNavigate, useParams } from "react-router-dom";
import useCart from "../hooks/useCart";
import useCheckout from "../hooks/useCheckout";
import { fetchCustomerProfile } from "../logic/fetch_customer_profile";
import { fetchCustomerPayment } from "../logic/fetch_customer_payment";
import { useEffect, useState } from "react";

export default function Confirmation() {
    // get:
    // - customer name
    // - the order id
    // - payment method (cardType last4 digit)

    const [firstName, setFirstName] = useState(null);
    const [lastName, setLastName] = useState(null);
    const [cardType, setCardType] = useState(null);
    const [last4, setLast4] = useState(null);
    const {orderId} = useParams();

    const getCustomerData = async () => {
        try {
            const customer = await fetchCustomerProfile();
            
            setFirstName(customer["first_name"]);
            setLastName(customer["last_name"]);
            
        } catch (e) {
            console.log(e);
        }
    }

    const getPaymentData = async () => {
        try {
            const payment = await fetchCustomerPayment(orderId);
            setCardType(payment["card_type"])
            setLast4(payment["last_4_digits"])

        } catch (e) {
            console.log(e)
        }
    }

    useEffect(() => {
        getCustomerData();
        getPaymentData();
    }, [])

    
    const { selectedItems } = useCart();
    const {subtotal, shippingFee, totalAmount} = useCheckout()
    const navigate = useNavigate()

    return (
        <>
        <h1>Your order has been placed successfully.</h1>
        <h4>Name on Card: {firstName} {lastName}</h4>
        <h4>Order ID: {orderId}</h4>
        <h4>Payment method: {cardType} {last4}</h4>

        <h4>Your orders:</h4>
        <table id="order-table">
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
        <h4>Subtotal: ${subtotal}</h4>
        <h4>Shipping fee: ${shippingFee}</h4>
        <h4>Total amount: ${totalAmount}</h4>
        <div class="options">
            <button class="button" onClick={() => navigate("/")}>Continue Shopping</button>
            <button class="button" onClick={() => navigate("/login")}>Log out</button>
        </div>
        
        </>
    )
}