import { Link} from "react-router-dom";
import useAuth from '../hooks/useAuth.js';
import { useEffect, useState } from "react";
import { fetchUserName } from "../logic/fetch_username.js";
import { fetchCustomerId } from "../logic/fetch_customer_id.js";
import useCustomer from "../hooks/useCustomer.js";

export default function Navbar() {
    const {isLoggedIn, logout} = useAuth();
    const [username, setUsername] = useState("");
    const {setCustomerId} = useCustomer();

    useEffect(() => {
        // upon login, fetch and set username and get customerId
        const fetchData = async () => {
            if (isLoggedIn) {
                try {
                    await fetchUserName(setUsername);
                    const customerId = await fetchCustomerId();
                    setCustomerId(customerId);
                } catch (error) {
                    console.error("Error fetching user data:", error);
                }
            }
        };
        fetchData();
    }, [isLoggedIn]);


    return (
        <nav className="nav">
        <a href="/"className="site-title">Jay Jay Mart</a>
        <ul>
            {isLoggedIn ? (
                <>
                  <li>
                     <Link to="/login">Hi, {username}!</Link>
                  </li>
                   
                  <li>
                     <Link onClick={logout}>Log out</Link>
                  </li>
                </>
                ) : (
                  <>
                    <li>
                       <Link to="/login">Log in</Link>
                    </li>
               
                    <li>
                       <Link to="/signup">Sign up</Link>
                    </li>
                  </>
                )}
            </ul>   
        </nav>
    );
}