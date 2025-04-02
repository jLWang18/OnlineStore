import { Navigate, Outlet } from "react-router-dom";
import useAuth from "../hooks/useAuth.js";

const RequireAuth = () => {
    const { isLoggedIn } = useAuth();

    // Is the user logged in? If yes, they can go to the desired protected page. 
    // If not, redirect them to the login page.
    return (
        isLoggedIn
        ? <Outlet></Outlet>
        : <Navigate to="/login"/>
    );
}

export default RequireAuth