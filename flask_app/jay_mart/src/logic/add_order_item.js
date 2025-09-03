import axios from "../api/axios";
import AxiosError from "../utils/AxiosError.js";

const ORDER_ITEM_URL = "http://localhost:5000/api/addOrderItem";

export async function addOrderItem(order_id, product_id, unit_price, quantity) {
     
    try {
        // add order item to the order item table
        const response = await axios.post(ORDER_ITEM_URL,
            JSON.stringify({order_id:order_id, product_id:product_id, 
                unit_price:unit_price, quantity:quantity}),
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
        // Handle axios error
        if (err.response) {
            // Handle error response from the server
            throw new AxiosError("Request failed", {
                status: err.response.status,
                data: err.response.data
            })
        } else {
            throw new Error('No response from server');
        }
    }
    
}