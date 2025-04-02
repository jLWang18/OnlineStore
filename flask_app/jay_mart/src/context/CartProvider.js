import { createContext, useState } from "react"

const CartContext = createContext({});

export const CartProvider = ({ children }) =>{

    // hold items selected by user in the array
    const [selectedItems, setSelectedItems] = useState([]);

    const onItemSelect = (item) => {
      
        // update the state of selected items based on the previous state
        setSelectedItems((prevSelected) => {
            // check if the item is already in the selected items list
            if (prevSelected.some((selected) => selected.product_id === item.product_id)) {
                // if the item is already selected, remove it (deselect)
                return prevSelected.filter((selected) => selected.product_id !== item.product_id);
            } else {
                // if the item is not selected, add it to the list (select)
                return [...prevSelected, item]
            }
        })
    }

    return (
        <CartContext.Provider value={{selectedItems, setSelectedItems, onItemSelect}}>
            {children}
        </CartContext.Provider>
    )

}

export default CartContext;