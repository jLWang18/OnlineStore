import './App.css';
import { useState, useEffect} from 'react';
import { Link, Outlet} from "react-router-dom";
import { displayTable, handleOrder } from './productTable.js';
import { validateLogin } from './login';


function HomeHeaders() {
  return (
    <div>
      <h1> Jay Jay Mart</h1>
      <p>where you can find what you need</p>
   </div>
  );
}

 function ProductTable() {
   // display products table
    useEffect(() => {
      displayTable()
    }, [])
    
    return (
      <>
      <table id="myTable">
        <thead>
          <tr>
              <th>Select</th>
              <th>Product ID</th>
              <th>Product Category</th>
              <th>Product Name</th>
              <th>Price</th>
              <th>Quantity</th>
          </tr>
        </thead>
        <tbody id="data-output">
        </tbody>
      </table>
      <button type="submit" onClick={handleOrder}>Add to Cart</button>
      </>
    )

}


export function LogIn() {
  // handle the states of input, initially input is empty ''
  const initialValues = {email: "", password: ""};
  const [formValues, setFormValues] = useState(initialValues);
  // Handle errors initially empty
  const [formErrors, setFormErrors] = useState({});
  // check if it is submitted
  const [isSubmit, setIsSubmit] = useState(false);

  const isValidEmail = (email) => {
    const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
  };

  const validateEmail = (emailInput) => {
  
    if (emailInput === '') {
      return false;
    } else if (!isValidEmail(emailInput)) {
      return false;
    }else if(emailInput.length < 13 || emailInput.length > 31) {
      return false;
    } else {
      return true;
    }

  }
  const validatePassword = (passwordInput) => {
      if(passwordInput === '') {
        return false;
      } else if(passwordInput.length < 8) {
        return false;
      } else {
        return true;
      }
    }
  const handleChange = (e) => {
    // get the field name and field value
    const { name, value } = e.target;
    // change the state of the value from empty to the current value
    setFormValues({...formValues, [name]: value});
  }

  const handleSubmit = (e) => {
    e.preventDefault();
    // validate email & password
    setFormErrors(validate(formValues));
    // set submit as true
    setIsSubmit(true)
    
  }
  useEffect(() => {
    console.log(formErrors);
    // if there is no eerror (i.e., if email & password is valid, display the homepage)
    if (Object.keys(formErrors).length === 0 && isSubmit) {
      // ...
    }
  })
  const validate = (values) => {
    const errors = {}

    const validEmail = validateEmail(values.email);
    const passwordValid = validatePassword(values.password);


    if (!validEmail){
      errors.email = 'Email must be at least between 13 and 31 characters';
    } 
    if (!passwordValid) {
      errors.password = 'Password must be at least 8 characters';
    }

    return errors
  }

  return (
    <div>
      <nav>
        <Link to="/">Home</Link>
        <Link to='/signup'>Sign up</Link>
      </nav>
      <br></br>
      <form onSubmit={handleSubmit}>
      <div className="input-control">
        {formErrors.email && <p className="error-message">{formErrors.email}</p>}
        <label htmlFor="email">Email</label>
        <input type="text" id="email" name="email" value={formValues.email} onChange={handleChange}/>
      </div>
      <div className="input-control">
       {formErrors.password && <p className="error-message">{formErrors.password}</p>}
        <label htmlFor="password">Password</label>
        <input type="text" id="password" name="password" value={formValues.password} onChange={handleChange}/>
      </div>
        <button type="submit">Log In</button>
        <Link to='/signup'>Don't have an account? Sign up here</Link>
      </form>
    </div>
  )
}

export function SignUp() {
  return (
  <div>
      <nav>
      <Link to="/">Home</Link>
      <Link to='/login'>Log in</Link>
    </nav>
  <form>
  <div className="input-control">
    <label htmlFor="fname">First Name</label>
    <input type="text" id="fname" name="fname"/>
  </div>
  <br/><br/>
  <div className="input-control">
    <label htmlFor="lname">Last Name</label>
    <input type="text" id="lname" name="lname"/>
  </div>
  <br/><br/>
  <div className="input-control">
    <label htmlFor="email">Email</label>
    <input type="text" id="email" name="email"/>
  </div>
  <div className="input-control">
    <label htmlFor="password">Password</label>
    <input type="text" id="password" name="password"/>
  </div>
  <br/><br/>
  <div className="input-control">
    <label htmlFor="phone">Phone</label>
    <input type="text" id="phone" name="phone"/>
  </div>
  <br/><br/>
  <button type="submit">Sign up</button>
  </form>
  </div>
  )
} 

function Home() {
  return (
    <>
      <nav className= "navDiv">
        <Link to="/login">Log in</Link>
        <Link to='/signup'>Sign up</Link>
    </nav>
      <HomeHeaders />
      <ProductTable />
      <Outlet />
   </>
  );

}
export function App() {
export function App() {
  return <Home />
}

export default App;
