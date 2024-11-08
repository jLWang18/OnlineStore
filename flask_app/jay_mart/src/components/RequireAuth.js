import { useLocation, Navigate, Outlet } from "react-router-dom";
import useAuth from "../hooks/useAuth";

const RequireAuth = () => {
    const { auth } = useAuth();
    const location = useLocation();

    // Is the user logged in? If yes, they can go to the desired protected page. 
    // If not, redirect them to the login page from the page they came from.
    return (
        auth?.accessToken
        ? <Outlet></Outlet>
        : <Navigate to="/login" state={{ from: location}} replace />
    );
}

export default RequireAuth