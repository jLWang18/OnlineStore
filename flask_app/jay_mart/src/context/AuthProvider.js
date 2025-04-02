import { createContext, useEffect, useState } from "react";

const AuthContext = createContext({});

export const AuthProvider = ({ children }) => {
    // Initialize `token` state with the token stored in localStorage (if any).
    const [token, setToken] = useState(localStorage.getItem("token"))

    // Initialize `isLoggedIn` state based on whether there is a `token` or not.
    const [isLoggedIn, setIsLoggedIn] = useState(!!token);
    
    // useEffect runs every time the `token` changes.
    useEffect(() => {
        if (token) {
            // If there's a `token`, store it in localStorage and set `isLoggedIn` to true.
            localStorage.setItem('token', JSON.stringify(token));
            setIsLoggedIn(true);

        } else {
             // If `token` is null, remove it from localStorage and set `isLoggedIn` to false.
            localStorage.removeItem('token');
            setIsLoggedIn(false)
        }
    }, [token]); // Dependency array with `token` ensures this runs when `token` changes.


     // `login` function updates the `token` state with a new token.
    const login = (newToken) => {
        setToken(newToken);
    };

     // `logout` function sets `token` to null, triggering `useEffect` cleanup of localStorage.
    const logout = () => {
        setToken(null);
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

