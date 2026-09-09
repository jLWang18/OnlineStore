import { useNavigate } from 'react-router-dom';
import  useCart  from '../hooks/useCart.js';
import '../styles/styles.css';
import useCheckout from '../hooks/useCheckout.js';
import { useEffect, useState } from 'react';
import { calculateOrder, createOrder } from '../logic/process_order.js';
import useCustomer from '../hooks/useCustomer.js';

export default function AddToCart() {
    const navigate = useNavigate();

    const {selectedItems} = useCart();

    
    const {subtotal, setSubtotal, shippingFee, setShippingFee, totalAmount, setTotalAmount} = useCheckout();

    const {customerId} = useCustomer();

    // user's specified quantity
    const [quantities, setQuantities] = useState({});

    const selections = []

    // for each product id
    for (let i = 0; i < selectedItems.length; i++) {
        const productIdVal = selectedItems[i].product_id
        const optionsList = []
        // 1 until stock qty
        for (let j = 1; j <= selectedItems[i].in_stock_quantity; j++) {
            const labelStr = String(j)
            const valueInt = j
            optionsList.push({label: labelStr, value: valueInt})
        }
        selections.push({productId: productIdVal, option: optionsList})

    }

    const selectProduct = (selection, prodId) => {
        // return selection object given the product_id
        return selection.productId === prodId
    }

    const handleQuantityChange = (productId, quantity) => {
        // productId = the ID of the product whose dropdown changed
        // quantity = the new value selected by the user
        setQuantities((prev) => ({
            // keep all the quantities that are already stored
            ...prev,

            // add/update the quantity for this specific product
            // example: if productId = 101 and quantity = "3",
            // this becomes: 101: 3
            [productId]: Number(quantity),
        }))
    }

    

    const addOrder = async () => {
        if (!customerId) {
            alert("Please log in before placing an order.")
            return
        }
        // store selected orders to items array of objects
        const orders = selectedItems.map(order => {
            // loop each order in the selection and parse it as object
            return {"product_id": order.product_id, 
                "unit_price": order.product_price,
                "quantity": quantities[order.product_id] || 1, 
            
        }})
        try {
            // create customer order
           const data = await createOrder(customerId, orders)

            // if successful, navigate to payment page
            navigate(`/payment/${data['order_id']}`)
        } catch (err) {
            if (err.response?.status === 400) {
                alert("one of the operations failed");
            } else if (err.response?.status === 500) {
                alert("The order could not be completed")
            }
        }
        
    }

    useEffect(() => {
        const calculateCustomerOrder = async (selectedItems, quantities) => {
            // store selected orders to items array of objects
            const orders = selectedItems.map(order => {
                // loop each order in the selection and parse it as object
                return {"product_id": order.product_id, 
                    "unit_price": order.product_price,
                    "quantity": quantities[order.product_id] || 1, 
                
            }})
            
            try {
                const receipt = await calculateOrder(orders)

                setSubtotal(receipt.data.subtotal)
                setShippingFee(receipt.data.shipping_fee)
                setTotalAmount(receipt.data.total_amount.toFixed(2))
            } catch (err) {
                alert(err)
            }

        }
        // calculate current seleccted order items
        calculateCustomerOrder(selectedItems, quantities)

    }, [selectedItems, quantities, setSubtotal, setShippingFee, setTotalAmount])
      

    return (
        <>
        <div className="display-container">
            <h1>Your Cart Items</h1>
            <table id="cart-table">
            <thead>
            <tr>
                <th>Product ID</th>
                <th>Product Category</th>
                <th>Product Name</th>
                <th>Price</th>
                <th>Stock</th>
                <th>Quantity</th>
            </tr>
            </thead>
            <tbody>
                {selectedItems.map((selectedItem) => {
                    return (
                        <tr key={selectedItem.product_id}>
                            <td>{selectedItem.product_id}</td>
                            <td>{selectedItem.product_category}</td>
                            <td>{selectedItem.product_name}</td>
                            <td>{selectedItem.product_price}</td>
                            <td>{selectedItem.in_stock_quantity}</td>
                            <td>
                                <select 
                                className="qty"
                                value={quantities[selectedItem.product_id] || 1}
                                onChange={(e) => handleQuantityChange(
                                    selectedItem.product_id,
                                    e.target.value
                                )}>
                                    {selections.find(selection => 
                                    selectProduct(selection, selectedItem.product_id)).option.map(option => {
                                        return (<option key={option.value}>{option.label}</option>)                          
                                    })}
                                </select>
                            </td>
                        </tr>
                    )
                })}
            </tbody>
        </table>
        
        <label><h4>items ({selectedItems.length}): ${subtotal}</h4></label>
        <label><h4>shipping: ${shippingFee}</h4></label>
        <label><h4>total: ${totalAmount}</h4></label>

        <div className="options">
            <button
                className="button"
                onClick={addOrder}
                disabled={!customerId}
            >
                Proceed to Payment
            </button>
            <button className="button" onClick={() => navigate("/")}>Cancel</button>
        </div>
        </div>
      </>
    );
}