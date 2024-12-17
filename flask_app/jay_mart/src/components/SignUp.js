import { useRef, useState, useEffect} from 'react'
import { validateFirstName, validateLastName, validateEmail, validatePassword, validatePhone } from '../logic/handle_inputs.js';
import { useNavigate, useLocation} from "react-router-dom";
import axios from '../api/axios.js';
import AxiosError from '../utils/AxiosError.js';

const SIGNUP_URL = "http://localhost:5000/api/signup"

const SignUp = () => {
  
  const [fname, setFirstName] = useState();
  const [lname, setLastName] = useState();
  const [email, setEmail] = useState();
  const [pwd, setPwd] = useState();
  const [phone, setPhone] = useState();

  const userRef = useRef();

  // Handle errors initially empty
  const [formErrors, setFormErrors] = useState({});

  // navigate user back to where they came from. 
  // Else, navigate to the home page by default 
  const navigate = useNavigate();
  const location = useLocation();
  const from = location.state?.from?.pathname || "/";

  const [isVerified, setVerified] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();

    const isValid = validate(fname, lname, email, pwd, phone);
    if (isValid === false) {
      alert("There is/are invalid input(s)")
      return;
    }

    // add new user to the database
    addCustomer(fname, lname, email, pwd, phone)
    .then(() => {
      // when signup is sucessful, go to the desired page
      navigate(from, {replace: true})
      setVerified(true)

    }).catch(err => {
      if (!err?.response) {
        alert("No server response");
      } else if (err.response?.status === 409) {
        alert("An email already exist in the database. Customer cannot add the same email");
      } else if (err.response?.status === 500) {
        alert("There was an issue adding new customer");
      }
      // after alert, should clear all the fields
      setFormErrors("")
      setFirstName("")
      setLastName("")
      setEmail("")
      setPwd("")
      setPhone("")
    })
  }
  useEffect(() => {
    if (isVerified) {
      console.log("sign up is sucessful")
    } else {
      console.error("sign up is not sucessful")
    }
  }, [isVerified])

  const validate = (fname, lname, email, pwd, phone) => {
    const errors = {}
    
    const validFirstName = validateFirstName(fname);
    const validLastName = validateLastName(lname);
    const validEmail = validateEmail(email);
    const validPassword = validatePassword(pwd);
    const validPhone = validatePhone(phone);

    if (!validFirstName) {
      errors.fname = 'First Name must contain alphabets only and at least between 3 and 50 characters';
    }

    if (!validLastName) {
      errors.lname = 'Last Name must contain alphabets only and at least between 3 and 150 characters'
    }
    
    if (!validEmail) {
      errors.email = 'Email must be at least between 13 and 31 characters';
    }

    if (!validPassword) {
      errors.password = 'Please enter a valid password at least 8 characters long, 1 uppercase letter, 1 lowercase letter, 1 number, and 1 symbol';

    }

    if (!validPhone) {
      errors.phone = 'Phone Number  must contain 10 digits';
    }
    
    // if there is/are invalid inputs, return false
    if (Object.keys(errors).length > 0) {
      setFormErrors(errors);
      return false;
    }

    return true;
  }

  async function addCustomer(fname, lname, email, pwd, phone) {
    try {
      // insert new customer to the database
      const response = await axios.post(SIGNUP_URL,
        JSON.stringify({first_name: fname, last_name: lname, email: email,
          password: pwd, phone_number: phone}), 
          {
            headers: {'Content-Type': 'application/json'},
            withCredentials: true

         })
      // if new customer is added to the database successfully, return true
      if (response.status >= 200 && response.status < 300) {
        return true

      } else {
        // if not successful, jump to the catch block
        throw new Error(`Unexpected status code: ${response.status}`)
      }
    } catch(err) {
      // Handle axios error
      if (err.response) {
        // Handle error response from the server
        throw new AxiosError("Request failed", {
          status: err.response.status,
          data: err.response.data
        })
      } else {
        throw new Error('No response from server');
      }
    }
    
  }

    return (
    <div>
    <form onSubmit={handleSubmit}>
    <div className="input-control">
      {formErrors.fname && <p className="error-message">{formErrors.fname}</p>}
      <label htmlFor="fname">First Name</label>
      <input type="text" id="fname" name="fname" ref={userRef} autoComplete="off" 
            onChange={(e) => setFirstName(e.target.value)} value={fname} required/>
    </div>
    <br/><br/>
    <div className="input-control">
      {formErrors.lname && <p className="error-message">{formErrors.lname}</p>}
      <label htmlFor="lname">Last Name</label>
      <input type="text" id="lname" name="lname" ref={userRef} autoComplete="off" 
            onChange={(e) => setLastName(e.target.value)} value={lname} required/>
    </div>
    <br/><br/>
    <div className="input-control">
      {formErrors.email && <p className="error-message">{formErrors.email}</p>}
      <label htmlFor="email">Email</label>
      <input type="text" id="email" name="email" ref={userRef} autoComplete="off" 
            onChange={(e) => setEmail(e.target.value)} value={email} required/>
    </div>
    <div className="input-control">
      {formErrors.password && <p className="error-message">{formErrors.password}</p>}
      <label htmlFor="password">Password</label>
      <input type="text" id="password" name="password" ref={userRef} autoComplete="off" 
            onChange={(e) => setPwd(e.target.value)} value={pwd} required/>
    </div>
    <br/><br/>
    <div className="input-control">
      {formErrors.phone && <p className="error-message">{formErrors.phone}</p>}
      <label htmlFor="phone">Phone</label>
      <input type="text" id="phone" name="phone" ref={userRef} autoComplete="off" 
            onChange={(e) => setPhone(e.target.value)} value={phone}  required/>
    </div>
    <br/><br/>
    <button type="submit">Sign up</button>
    </form>
    </div>
    )
  }

  export default SignUp