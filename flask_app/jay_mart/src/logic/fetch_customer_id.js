import axios from "../api/axios";

const PROFILE_URL = "http://localhost:5000/api/getProfile"

export const fetchCustomerId = async() => {
  // get access token
  const token = localStorage.getItem("token");

  try {
    const response = await axios.get(PROFILE_URL,
      {
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
          },
          withCredentials: true
        
      });
    
    // get the customer profile
    const customer = response.data

    // get and set the customer id
    return customer["customer_id"]

  } catch(err) {
      throw err
    }
    
  }

