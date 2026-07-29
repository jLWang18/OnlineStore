function fetchOrderList(customer_id) {
    // when the orders sucessfully fetched, 
    // return array as resolved value
    return new Promise((resolve, reject) => {
        // first, resolve the request.
        fetch(`http://localhost:5000/api/getAllOrders/${customer_id}`).then(response => {
            // If the request is not successful, return error.
            // If successful, return the JSON response
            if (!response.ok) {
                throw new Error(`HTTP error status: ${response.status}`)
            }
            return response.json();
        
        }).then(ordersObj => {
            // secondly, upon successful request, 
            //  get the array of orders 
            resolve(ordersObj.data)
        // else, reject the promise 
        }).catch (error => {
            reject(error);
        })
    })

}

// resolve order list request with an array. Else, display fetching error
export async function getOrderList(customer_id) {
    try {
       const orderList = await fetchOrderList(customer_id)
       return orderList  
    } catch(error) {
        console.log("Error fetching data: ", error)
    } 
   
}

// fetch an order of a customer given the order_id
function fetchOrder(order_id) {
    // Promise: get an order
    return new Promise((resolve, reject) => {
        // resolve the request
        fetch(`http://localhost:5000/api/getOrder/${order_id}`).then(response => {
            // if request is not successful, return error
            if (!response.ok) {
                throw new Error(`HTTP error status: ${response.status}`)
            }
            // If successful, converts the HTTP response body into a JavaScript object
            return response.json()

        }).then(orderObj => {
            // upon successful request, get the order data
            resolve(orderObj)
        // else, reject the promise
        }).catch(error => {
            reject(error)
        })
    })
}

// resolve an order retrieval request. Eslse, display fetching error
export async function getOrder(order_id) {
    try {
        const order = await fetchOrder(order_id)
        
        // access the "data" property from the JSON response
        return order.data 
    } catch (error) {
        console.log("Error fetching data: ", error)
    } 
}