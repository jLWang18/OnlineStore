import axios from "../api/axios";
const ORDER_ITEMS_URL = "http://localhost:5000/api/addAllOrderItems";

export async function addAllOrderItems(order_id, items) {
     
    try {
        const response = await axios.post(ORDER_ITEMS_URL,
            { order_id, items },
                {
                    headers: {'Content-Type': 'application/json'},
                    withCredentials: true
                }
        );

        // if order item is added to the database successfully, return true
        if (response.status >= 200 && response.status < 300) {
            return true
        } else {
            // if not successful, jump to the catch block
            throw new Error(`Unexpected status code: ${response.status}`)
        }

    } catch (err) {
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