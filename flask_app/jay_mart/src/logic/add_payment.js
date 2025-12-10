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
        const returned_order_id = response.data.order_id
       
        // if payment info is added to the database successfully, return the order id
        if (response.status >= 200 && response.status < 300) {
            return returned_order_id
        } else {
            // if not successful, jump to the catch block
            throw new Error(`Unexpected status code: ${response.status}`)
        }

    } catch (err) {
        // handle axios response
        if (err.response) {
            // handle axios response from the server
            throw new AxiosError("Request failed", {
                status: err.response.status,
                data: err.response.data
            })
        } else {
            throw new Error("No response from server")
        }
    }
}