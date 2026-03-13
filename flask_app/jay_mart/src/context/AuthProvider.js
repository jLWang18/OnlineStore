import { createContext, useState } from "react";
import useCart from "../hooks/useCart";
import { useNavigate } from "react-router-dom";

const AuthContext = createContext({});

export const AuthProvider = ({ children }) => {
    // Initialize `token` state with the token stored in localStorage (if any).
    const [token, setToken] = useState(localStorage.getItem("token"))

    // Initialize `isLoggedIn` state based on whether there is a `token` or not.
    const [isLoggedIn, setIsLoggedIn] = useState(!!token);

    const {selectedItems, onItemSelect} = useCart();

     const navigate = useNavigate();
    
    // `login` function updates the `token` state with a new token.
    const login = (newToken) => {
        // store access token
        localStorage.setItem('token', JSON.stringify(newToken));

        // update state
        setToken(token)
        setIsLoggedIn(true);
    };

     // `logout` function sets `token` to null, triggering `useEffect` cleanup of localStorage.
    const logout = () => {
        
        // loop through selected items
        selectedItems.forEach(item => {
        // for each item in eselected items, deselect item
        onItemSelect(item)
        
        });
      
        // remove token from storage
        localStorage.removeItem('token');

        // update state
        setToken(token)
        setIsLoggedIn(false)

        // navigate to home page
        navigate('/')

        
    };
    
    // Provide `token`, `isLoggedIn`, `login`, and `logout` to all child components
    // that consume this context.
    return (
        <AuthContext.Provider value={{token, isLoggedIn, login, logout}}>
            {children}
        </AuthContext.Provider>
    )
}

export default AuthContext;

