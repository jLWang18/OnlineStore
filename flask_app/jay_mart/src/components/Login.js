import { useRef, useState, useEffect} from 'react'
import { Link, useNavigate, useLocation} from "react-router-dom";
import { validateEmail, validatePassword } from '../logic/handle_inputs.js';
import useAuth from '../hooks/useAuth.js';
import axios from '../api/axios.js';

const LOGIN_URL = "http://localhost:5000/api/login"

const Login = () => {
    const { setAuth } = useAuth();
  
    // navigate user back to where they came from. 
    // Else, navigate to the home page by default 
    const navigate = useNavigate();
    const location = useLocation();
    const from = location.state?.from?.pathname || "/";
  
    const userRef = useRef();
  
    const [email, setEmail] = useState();
    const [pwd, setPwd] = useState();
    const [isLoading, setIsLoading] = useState(false);
   
    // Handle errors initially empty
    const [formErrors, setFormErrors] = useState({});
    // check if it is submitted
    const [isSubmit, setIsSubmit] = useState(false);
  
    
  
    const handleSubmit =  async (e) => {
      e.preventDefault();
      // validate email & password. 
      // if the form is validated, then proceed to authentication. If not, just return
      if (!validate(email, pwd)) {
        return
      } 
  
      setIsLoading(true);
      
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
        console.log(JSON.stringify(response?.data));
        const accessToken = response?.data?.accessToken;
        setAuth(accessToken);
        localStorage.setItem("accessToken", accessToken);
        // upon successful login, user can go to the desired page 
        navigate(from, {replace: true})
  
      } catch(err) {
        if (!err?.response) {
          alert('No Server Response');
        } else if (err.response?.status === 400) {
          alert('Misiing email or password');
        } else if (err.response?.status === 401) {
          alert("Unauthorized: Either email or password is not valid");
          // TODO: after alert, should clear all the fields
  
        } else {
          alert('Login Failed')
        }
  
      }
      // set submit as true
      setIsSubmit(true)
  }
    
    useEffect(() => {
      // if there is no eerror (i.e., if email & password is valid, display the homepage)
      if (Object.keys(formErrors).length === 0 && isSubmit) {
      console.log("Logged in sucessfully")
      }
    })
  
    const validate = (email, pwd) => {
      const errors = {}
  
      const validEmail = validateEmail(email);
      const validPassword = validatePassword(pwd);
  
  
      if (!validEmail){
        errors.email = 'Email must be at least between 13 and 31 characters';
      } 
      if (!validPassword) {
        errors.password = 'Password must be at least 8 characters';
      }
  
      setFormErrors(errors)
      // return true if no errors. Else, return false
      return Object.keys(formErrors).length === 0
    }
  
    return (
      <div>
        <form onSubmit={handleSubmit}>
          <div className="input-control">
            {formErrors.email && <p className="error-message">{formErrors.email}</p>}
            <label htmlFor="email">Email</label>
            <input type="text" id="email" name="email" ref={userRef} autoComplete="off" 
            onChange={(e) => setEmail(e.target.value)} value={email} required/>
          </div>
          <div className="input-control">
          {formErrors.password && <p className="error-message">{formErrors.password}</p>}
            <label htmlFor="password">Password</label>
            <input type="password" id="password" name="password" ref={userRef} 
            onChange={(e) => setPwd(e.target.value)} value={pwd} required/>
          </div>
          <button type="submit">Log In</button>
          <Link to='/signup'>Need an account? Sign up</Link>
        </form>
      </div>
    )
  }
  export default Login
  