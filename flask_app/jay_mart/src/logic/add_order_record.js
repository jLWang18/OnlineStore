import axios from "../api/axios";
import AxiosError from '../utils/AxiosError.js'

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
        
        // // if order record is added to the database successfully, return true
        // if (response.status >= 200 && response.status < 300) {
        //     return true
        // } else {
        //     // if not successful, jump to the catch block
        //     throw new Error(`Unexpected status code: ${response.status}`)
        // }
    
    } catch(err) {
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