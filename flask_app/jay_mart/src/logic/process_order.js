import axios from "../api/axios";
const CREATE_ORDER_URL = "http://localhost:5000/api/createOrder";
const GET_ORDER_TOTAL_URL = "http://localhost:5000/api/calculateOrder";

export async function createOrder(customer_id, orders) {
     
    try {
        const response = await axios.post(CREATE_ORDER_URL,
            JSON.stringify({customer_id: customer_id, orders: orders}),
                {
                    headers: {'Content-Type': 'application/json'},
                    withCredentials: true
                }
        );
        return response.data.data

    } catch (err) {
        throw err
    }
    
}

export async function calculateOrder(orders) {
    try {
        // calculate order items (subtotal, shipping fee, and total amounts)
        const receipt = await axios.post(GET_ORDER_TOTAL_URL, {orders}, 
            {
               headers: {'Content-Type': 'application/json'},
               withCredentials: true
            }
        )
        return receipt

    } catch (err) {
        throw err
    }
}
    