import axios from "../api/axios";

export const fetchCustomerPayment = async(order_id) => {
    if (!order_id) {
        throw new Error("Order ID is required.")
    }
    try {
        const response = await axios.get(`http://localhost:5000/api/getPayment/${order_id}`)

        const payment = response.data

        return payment
        
    } catch(err) {
       // Server responded with error (404, 401, 500)
        if (err.response) {
            console.error("Server Errorr here")
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