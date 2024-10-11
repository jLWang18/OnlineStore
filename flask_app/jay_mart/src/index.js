import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import { App, LogIn, SignUp } from './App';
import { BrowserRouter, Routes, Route } from "react-router-dom"; 

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
 <BrowserRouter>
   <Routes>
     <Route path='/' element={<App />}/>
     <Route path='/login' element={<LogIn />}/>
     <Route path='/signup' element={<SignUp/>}/>
   </Routes>
  </BrowserRouter>
);
