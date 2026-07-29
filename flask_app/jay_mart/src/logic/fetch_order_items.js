import axios from "../api/axios"

function getOrderItems(order_id) {
    // promise: get all order items
    return new Promise((resolve, reject) => {
        fetch(`http://localhost:5000/api/getAllOrderItems/${order_id}`).then(response => {
            // if response is not successful, return error
            if (!response.ok) {
                throw new Error(`HTTP error status: ${response.status}`)
            }
            // if successful, converts the HTTP response body into a JavaScript object
            return response.json()
        }).then(itemsObj => {
            // upon successful request, get order items
            resolve(itemsObj)
            // else, reject the promise
        }).catch(error => {
            reject(error)
        })
    })
}

export async function fetchItems (order_id) {
  try {
    const items = await getOrderItems(order_id)
    return items.data
  } catch (error) {
    console.log("Error fetching data: ", error)
  }

}