import { useContext } from "react";
import CheckoutContext from "../context/CheckoutProvider";

const useCheckout = () => {
    return useContext(CheckoutContext)
}
export default useCheckout;