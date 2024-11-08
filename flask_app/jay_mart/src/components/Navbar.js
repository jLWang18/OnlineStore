import { Link} from "react-router-dom";
import useAuth from '../hooks/useAuth.js';

export default function Navbar() {
    const { isLoggedIn, token } = useAuth()

    console.log("isLoggedIn = " + isLoggedIn)

    return (
        <nav className="nav">
        <a href="/"className="site-title">Jay Jay Mart</a>
        <ul>
            {isLoggedIn ? (
                <>
                <li>
                   <Link to="/login">Hi, there!</Link>
               </li>

                </>
                ): (
                <li>
                   <Link to="/login">Log in</Link>
               </li>
            )}
            
            <li>
                <Link to="/signup">Sign up</Link>
            </li>
         </ul>   
      </nav>
    );
}