import { Link} from "react-router-dom";
import useAuth from '../hooks/useAuth.js';
import { useEffect, useState } from "react";
import { fetchUserName } from "../logic/fetch_username.js";

export default function Navbar() {
    const {isLoggedIn, logout} = useAuth();
    const [username, setUsername] = useState("");

    useEffect(() => {
        // if the user is logged in, fetch username. Else, return 
        if (isLoggedIn) {
            fetchUserName(setUsername);
        } else {
            return
        }
        
    }, [isLoggedIn])


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