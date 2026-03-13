import axios from "../api/axios";

const ORDER_RECORD_URL = "http://localhost:5000/api/addOrderRecord"

export async function addOrderRecord (customer_id, subtotal, shipping_fee, total_amount) {
    try {
        // add order to the order_record table
        const response = await axios.post(ORDER_RECORD_URL,
            JSON.stringify({customer_id: customer_id, subtotal: subtotal, shipping_fee: shipping_fee, total_amount: total_amount}),
            {
                headers: {'Content-Type': 'application/json'},
                withCredentials: true
            }
        );

        const order_id = response.data

        return order_id
    
    } catch(err) {
         // Server responded with error (404, 401, 500)
        if (err.response) {
            console.error("Server Error here")
            throw {
                status: err.response.status,
                message: err.response.data?.error || "Server error",
            };
        }
        // Network / CORS / Server down
        throw {
            status: 0,
            message: "Unable to reach server",
        };

    }
    
}