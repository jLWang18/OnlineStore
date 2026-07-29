import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { getOrderList } from "../logic/fetch_orders_info.js";

export default function Profile() {
    const [orders, setOrders] = useState([]);
    const {customerId} = useParams()


    useEffect(() => {
        const fetchOrders = async () => {
            // fetch all orders
            const ordersData = await getOrderList(customerId);
            // set state with fetched orders array
            setOrders(ordersData);
        };
        // call this method
        fetchOrders();

    }, [customerId])

    return (
        <>
        <div className="display-container">
            <h1>Your Orders</h1>
            <table id="order-table">
                <thead>
                    <tr>
                        <th>Order Number</th>
                        <th>Order Date</th>
                        <th>Payment Status</th>
                        <th>Order Total</th>
                    </tr>
                </thead>
                <tbody>
                    {orders.map((order) => {
                        return (
                            <tr key={order.order_id}>
                                <td><Link to={`orderSummary/${order.order_id}`}>{order.order_id}</Link></td>
                                <td>{order.order_date}</td>
                                <td>{order.payment_status}</td>
                                <td>{order.order_total}</td>
                            </tr>
                        )
                    })}
                </tbody>
            </table>
        </div>
        </>
    )
}
