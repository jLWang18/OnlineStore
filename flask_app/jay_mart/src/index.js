import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import { App } from './App';
import { BrowserRouter} from 'react-router-dom'; 
import { AuthProvider } from './context/AuthProvider';
import { CartProvider } from './context/CartProvider';
import { CheckoutProvider } from './context/CheckoutProvider';
import "./styles/styles.css";
import { CustomerProvider } from './context/CustomerProvider';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <BrowserRouter>
    <CustomerProvider>
      <CartProvider>
        <AuthProvider> 
          <CheckoutProvider>   
            <App />
          </CheckoutProvider>     
        </AuthProvider>
      </CartProvider>
    </CustomerProvider>
  </BrowserRouter>
  
);
