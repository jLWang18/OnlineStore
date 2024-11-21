import { Link} from "react-router-dom";
import useAuth from '../hooks/useAuth.js';
import { useEffect, useState } from "react";
import axios from "../api/axios.js";

const WHOAMI_URL = "http://localhost:5000/api/whoami"

export default function Navbar() {
    const {isLoggedIn, logout} = useAuth();
    const [username, setUsername] = useState("");

    useEffect(() => {
        if (!isLoggedIn) return;

        const fetchUserName = async() => {
            
            const token = localStorage.getItem("token");
            if (!token) {
                console.error("No token found");
                return;
            }

            try {

                const response = await axios.get(WHOAMI_URL,
                    {
                        headers: {
                            'Content-Type': 'application/json',
                            Authorization: `Bearer ${localStorage.getItem("token")}`
                        },
                        withCredentials: true
            
                    });

                // get the username
                const userData = response.data
                // set the username
                setUsername(userData.data)

            } catch (err) {
                if (!err?.response) {
                    alert('No Server Response Navbar');
                  } else if (err.response?.status === 401) {
                    alert('Authorization token is missing');
                  } else {
                    alert("There was an issue in getting username");
                  }
            }
        }
        // if the user is logged in, then fetch the username
        if (isLoggedIn) {
            fetchUserName();
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
                ): (
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