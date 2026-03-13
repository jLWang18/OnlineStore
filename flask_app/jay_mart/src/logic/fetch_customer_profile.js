import axios from "../api/axios";

const PROFILE_URL = "http://localhost:5000/api/getProfile"

export const fetchCustomerProfile = async() => {
  // get access token
  const token = localStorage.getItem("token");
  if (!token) {
    console.error("You're not logged in.")
    return;
  }
  
  // get customer's first name based on access token
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

    return customer

  } catch(err) {
     // Server responded with error (404, 401, 500)
        if (err.response) {
            console.error("Server Error here")
            throw {
                status: err.response.status,
                message: err.response.data?.error || "Server error",
            };
        }
        // Network / CORS / Server down
        throw {
            status: 0,
            message: "Unable to reach server",
        };

    }
    
  }

