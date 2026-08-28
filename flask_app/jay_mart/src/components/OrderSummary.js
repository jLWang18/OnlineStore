import { useParams } from "react-router-dom"
import { useEffect, useState } from "react"
import { getOrder } from "../logic/fetch_orders_info"
import { fetchCustomerPayment } from "../logic/fetch_customer_payment"
import { fetchItems } from "../logic/fetch_order_items"

export default function OrderSummary() {
    const {orderId} = useParams()

    const [orderDate, setOrderDate] = useState(null)
    const [orderNumber, setOrderNumber] = useState(null)
    const [subtotal, setSubtotal] = useState(null)
    const [shippingFee, setShippingFee] = useState(null)
    const [totalAmount, setTotalAmount] = useState(null)

    const [cardType, setCardType] = useState(null)
    const [last4, setLast4] = useState(null)

    const [items, setOrderItems] = useState([])

    useEffect(() => {
        const fetchOrderInfo = async () => {
            const order = await getOrder(orderId)
            setOrderDate(order["order_date"])
            setOrderNumber(order["order_number"])
            setSubtotal(order["subtotal"])
            setShippingFee(order["shipping_fee"])
            setTotalAmount(order["total_amount"])

        }

        const fetchPaymentInfo = async () => {
            const payment = await fetchCustomerPayment(orderId)
            setCardType(payment["card_type"])
            setLast4(payment["last_4_digits"]) 

        }

        const fetchOrderItems = async () => {
            const items = await fetchItems(orderId)
            setOrderItems(items)
        }
        fetchOrderInfo()
        fetchPaymentInfo()
        fetchOrderItems()
        
    }, [orderId])

    return  (
        <>
        <div className="OS-title">
            <h1 style={{textAlign: 'center'}}>Order Summary</h1>
        </div>
        <div className="order-info">
            <h4>Order Date: {orderDate}</h4>
            <h4>Order Number: {orderNumber}</h4>
            <h4>Payment Method: {cardType} {last4}</h4>
        </div>
        <div className="purchased-items">
            <h2> Purchased Items</h2>
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
                    {items.map((item) => (
                        <tr key={item.product_id}>
                            <td>{item.product_id}</td>
                            <td>{item.product_category}</td>
                            <td>{item.product_name}</td>
                            <td>{item.product_price}</td>
                            <td>{item.product_quantity}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
            <div className="total-order">
                <h4>Subtotal: ${subtotal}</h4>
                <h4>Shipping fee: ${shippingFee}</h4>
                <h4>Total amount: ${totalAmount}</h4>
            </div>
        </div>
        
        </>

    )
}