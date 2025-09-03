import axios from "../api/axios";

const PROFILE_URL = "http://localhost:5000/api/getProfile"

export const fetchCustomerId = async() => {
  // get access token
  const token = localStorage.getItem("token");
  if (!token) {
    console.error("You're not logged in.")
    return;
  }
  
  // get customer id based on access token
  try {
    const response = await axios.get(PROFILE_URL,
      {
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem("token")}`
          },
          withCredentials: true
        
      });
    
    // get the customer profile
    const customer = response.data

    // get and set the customer id
    return customer["customer_id"]

  } catch(err) {
    // if (!err?.response) {
    //   alert('No Server Response Navbar');
    // } else if (err.response?.status === 401) {
    //   alert('Authorization token is missing');
    // } else {
    //   alert("There was an issue in getting customer id");
    // }
      const errorMsg = err.response?.data?.error || 'An unexpected error occurred';
      alert(errorMsg); // No need to rewrite the message here

    }
    
  }

