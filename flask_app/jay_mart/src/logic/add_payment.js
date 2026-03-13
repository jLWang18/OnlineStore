import axios from "../api/axios"
import AxiosError from "../utils/AxiosError"

const PAYMENT_URL = "http://localhost:5000/api/addPayment"

export async function addPayment(customer_id, order_id, total_price, last_4_digits, card_type) {
    try {
        // add customer's payment info to the payment database
        const response = await axios.post(PAYMENT_URL,
            JSON.stringify({customer_id: customer_id, order_id: order_id, 
                total_price: total_price, last_4_digits: last_4_digits, card_type: card_type}),
                {
                    headers: {'Content-Type' : 'application/json'},
                    withCredentials: true
                }
            
        )
        return response.data

    } catch (err) {
        throw err
    }
}