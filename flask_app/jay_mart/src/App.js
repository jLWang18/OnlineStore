import Home from './components/Home.js';
import Login from './components/Login.js';
import SignUp from './components/SignUp.js';
import Navbar from './components/Navbar.js';
import {Routes, Route} from "react-router-dom";
import AddToCart from './components/AddToCart.js';
import Payment from './components/Payment.js';
import RequireAuth from './components/RequireAuth.js';



export function App() {
  return (
    <>
      <Navbar/>
      <div className="container">
        <Routes>
          {/* public routes */}
          <Route path="/" element={<Home />}/>
          <Route path="/login" element={<Login />}/>
          <Route path="/signup" element={<SignUp />}/>

          {/* protected routes */}
          <Route element={<RequireAuth />}>
            <Route path="/addtocart" element={<AddToCart />}/>
            <Route path="/payment" element={<Payment />}/>
          </Route>

        </Routes>
      </div>
   </>
  );
}

export default App;
