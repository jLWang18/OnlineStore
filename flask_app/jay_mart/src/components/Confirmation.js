import { useNavigate, useParams } from "react-router-dom";
import useCart from "../hooks/useCart";
import useCheckout from "../hooks/useCheckout";
import { useState, useEffect } from "react";
import {fetchCustomerProfile} from "../logic/fetch_customer_profile";
import {fetchCustomerPayment} from "../logic/fetch_customer_payment";
import { fetchOrderStatus } from "../logic/fetch_order_status";
import useAuth from "../hooks/useAuth";

export default function Confirmation() {
    
    const [firstName, setFirstName] = useState(null);
    const [lastName, setLastName] = useState(null);
    const [cardType, setCardType] = useState(null);
    const [last4, setLast4] = useState(null);
    const {orderId} = useParams();

    const {logout} = useAuth()

    const getPaymentData = async () => {
        try {
            const payment = await fetchCustomerPayment(orderId);
            setCardType(payment["card_type"])
            setLast4(payment["last_4_digits"])
        } catch (e) {
            console.log(e)
        }
    }

     const getCustomerData = async () => {
        try {
            const customer = await fetchCustomerProfile();
            
            setFirstName(customer["first_name"]);
            setLastName(customer["last_name"]);
            
        } catch (e) {
            console.log(e);
        }
    }

     useEffect(() => {
        const fetchStatus = async () => {
            const status = await fetchOrderStatus(orderId);

            if (status !== "PAID") {
                navigate("/");
            } else {
                getCustomerData();
                getPaymentData();
            }
        }

        fetchStatus()
    
    }, [])
    
    const { selectedItems } = useCart();
    const {subtotal, shippingFee, totalAmount} = useCheckout()
    const navigate = useNavigate()

    return (
        <div className="confirmation">
            <h1>Your order has been placed successfully.</h1>
            <h4>Full name: {firstName} {lastName}</h4>
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
                    {selectedItems.map((item) => (
                        <tr key={item.product_id}>
                            <td>{item.product_id}</td>
                            <td>{item.product_category}</td>
                            <td>{item.product_name}</td>
                            <td>{item.product_price}</td>
                            <td>{item.in_stock_quantity}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
            <h4>Subtotal: ${subtotal}</h4>
            <h4>Shipping fee: ${shippingFee}</h4>
            <h4>Total amount: ${totalAmount}</h4>
            <div className="options">
                <button className="button" onClick={() => navigate("/")}>
                    Continue Shopping
                </button>
                <button className="button" onClick={logout}>
                    Log out
                </button>
            </div>
        </div>
    );
}