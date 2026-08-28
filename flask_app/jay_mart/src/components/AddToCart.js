import { useNavigate } from 'react-router-dom';
import  useCart  from '../hooks/useCart.js';
import '../styles/styles.css';
import useCheckout from '../hooks/useCheckout.js';
import { useEffect, useState } from 'react';
import { addOrderRecord } from '../logic/add_order_record.js';
import { addAllOrderItems } from '../logic/add_all_order_items.js';
import useCustomer from '../hooks/useCustomer.js';

const SHIPPING_COST = 4.99

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
        
        // add customer's id, subtotal, shippingFee, and total price to the order_record table
        const orderId = await addOrderRecord(customerId, subtotal, shippingFee, totalAmount)
        

        // store selected orders to items array of objects
        const items = selectedItems.map(order => {
            // loop each order in the selection and parse it as object
            return {"product_id": order.product_id, 
                   "quantity": quantities[order.product_id] || 1, 
                   "unit_price": order.product_price
                } 
        })
        
        // add all orders to order item table
        await addAllOrderItems(orderId, items)
        

        // navigate to payment page
        navigate(`/payment/${orderId}`)

        
    }

    useEffect(() => {
        // calculate subtotal (without shipping cost) and totalAmount (with shipping cost) 
        const itemsTotalPrice = (selectedItems) => {
            
            // loop thrrough selectedItems array and calculate total prices
            let subtotal = 0;
            for (let i = 0; i < selectedItems.length; i++) {
                // subtotal amount of an item = price * quantity
                subtotal += selectedItems[i].product_price * (quantities[selectedItems[i].product_id] || 1);

            }
            // round up to two decimal places
            subtotal = Number(subtotal.toFixed(2));
             // total price of an item = subtotal + shipping cost
            const totalAmount = Number((subtotal + SHIPPING_COST).toFixed(2));

            setSubtotal(subtotal)
            setShippingFee(SHIPPING_COST)
            setTotalAmount(totalAmount)
        }

        itemsTotalPrice(selectedItems);

    }, [selectedItems, setSubtotal, setShippingFee, setTotalAmount, quantities])
      

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
        <label><h4>subtotal: ${totalAmount}</h4></label>

        <div className="options">
            <button className="button" onClick={() => addOrder()}>Proceed to Payment</button>
            <button className="button" onClick={() => navigate("/")}>Cancel</button>
        </div>
        </div>
      </>
    );
}