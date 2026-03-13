import { useState, useEffect} from 'react'
import { Link, useNavigate, useLocation} from "react-router-dom";
import { validateEmail, validatePassword } from '../logic/handle_inputs.js';
import useAuth from '../hooks/useAuth.js';
import axios from '../api/axios.js';
import AxiosError from '../utils/AxiosError.js'
import '../styles/styles.css';
import { fetchCustomerId } from '../logic/fetch_customer_id.js';
import useCustomer from '../hooks/useCustomer.js';

const LOGIN_URL = "http://localhost:5000/api/login"

const Login = () => {
    const { login } = useAuth();
  
    // navigate user back to where they came from. 
    // Else, navigate to the home page by default 
    const navigate = useNavigate();
    const location = useLocation();
    const from = location.state?.from?.pathname || "/";
  
    const [email, setEmail] = useState("");
    const [pwd, setPwd] = useState("");
    const [isVerified, setVerified] = useState(null);
   
    // Handle errors initially empty
    const [formErrors, setFormErrors] = useState({});

    const {setCustomerId} = useCustomer();
  
    
  
    const handleSubmit =  async (e) => {
      e.preventDefault();
      // validate email & password. 
      // if the form is validated, then proceed to authentication. If not, just return
      const isValid = validate(email, pwd);
      if (isValid === false) {
        alert("There is/are invalid input(s)")
        return;
      }

      try {
        // 1. verify credentials
        const accessToken = await verify(email, pwd)
        if (!accessToken) throw new Error("login failed")
        
        // 2. store token / update auth state
        login(accessToken)
 
        // 3. fetch and set customer's id 
        const customerId = await fetchCustomerId()
        setCustomerId(customerId)

        // 4. mark verified
        setVerified(true)

        // 5. navigate to the desired page
        navigate(from, {replace: true})

        // 6. clear form after success
        setFormErrors("")
        setEmail("")
        setPwd("")
       
        
      } catch (err) {
        if (!err?.response) {
          alert('No Server Response');
        } else if (err.response?.status === 400) {
          alert('Misiing email or password');
        } else if (err.response?.status === 401) {
          alert("Unauthorized: Either email or password is not valid");
        }
      }
    }

    const validate = (email, pwd) => {
      const errors = {};
  
      const validEmail = validateEmail(email);
      const validPassword = validatePassword(pwd);
  
      if (!validEmail) {
        errors.email = 'Email must be at least between 13 and 31 characters';
      } 
      
      if (!validPassword) {
        errors.password = 'Password must be at least 8 characters';
      } 
      
      if (Object.keys(errors).length > 0) {
        setFormErrors(errors);
        return false;
      }
      
      return true;

    }

    async function verify(email, pwd) {
      // handle user authentication
      try {
        // send user input as JSON format
        const response = await axios.post(LOGIN_URL, 
          JSON.stringify({email: email, password: pwd}),
          {
            headers: {'Content-Type': 'application/json'},
            withCredentials: true
            
          }
        );
        
        const accessToken = response.data;
        return accessToken

      } catch(err) {
        throw err
     }
  
    }

    useEffect(() => {
      if (isVerified === null) return; // don't run anything on initial load

      // if there is no error (i.e., if email & password is valid, display the homepage)
      if (isVerified) {
        console.log("Logged in sucessfully")

      } else{
        console.error("Log in is not sucessful")
      }
    },[isVerified])

  
  
    return (
      <div>
        <form onSubmit={handleSubmit}>
          <div class='input-control'>
              <div class="input-control-email">
                {formErrors.email && <p class="error-message">{formErrors.email}</p>}
                <label htmlFor="email">Email</label>
                <input type="text" id="email" name="email" autoComplete="off" 
              onChange={(e) => setEmail(e.target.value)} value={email} required/>
              </div>
              <div class="input-control-password">
                {formErrors.password && <p class="error-message">{formErrors.password}</p>}
                <label htmlFor="password">Password</label>
                <input type="password" id="password" name="password" 
                onChange={(e) => setPwd(e.target.value)} value={pwd} required/>
              </div>
            <div class='options'>
              <button class='button' type="submit">Log In</button>
              <Link to='/signup'>Need an account? Sign up</Link>
            </div>
          </div>
        </form>
      </div>
    )
  }
  export default Login
  