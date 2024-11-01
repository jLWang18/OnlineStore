import { Link} from "react-router-dom";

export default function Navbar() {

    return <nav className="nav">
        <a href="/"className="site-title">Jay Jay Mart</a>
        <ul>
            <li>
                <Link to="/login">Log in</Link>
            </li>
            <li>
                <Link to="/signup">Sign up</Link>
            </li>
            
        </ul>
    </nav>
}