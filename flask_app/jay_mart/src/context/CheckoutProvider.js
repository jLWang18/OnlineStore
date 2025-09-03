import { createContext, useState} from "react";

const CheckoutContext = createContext({});

export const CheckoutProvider = ({ children }) => {
    
    // total price of all items in the order (excluding shipping cost)
    const [subtotal, setSubtotal] = useState(0);

    // shipping fee applied to the order
    const [shippingFee, setShippingFee] = useState(0);

    // Final total price of the order (including shipping cost)
    const [totalAmount, setTotalAmount] = useState(0);

    return (
        <CheckoutContext.Provider value={{subtotal, setSubtotal, shippingFee, setShippingFee, totalAmount, setTotalAmount}}>
            {children}
        </CheckoutContext.Provider>
    )
}
export default CheckoutContext
