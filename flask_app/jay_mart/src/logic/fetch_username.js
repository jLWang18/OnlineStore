import axios from "../api/axios.js";

const WHOAMI_URL = "http://localhost:5000/api/whoami"

export const fetchUserName = async(setUsername) => {
            
    const token = localStorage.getItem("token");
    if (!token) {
        console.error("No token found");
        return;
    }

    try {

        const response = await axios.get(WHOAMI_URL,
            {
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${localStorage.getItem("token")}`
                },
                withCredentials: true
    
            });

        // get the username
        const userData = response.data
        // set the username
        setUsername(userData.data)

    } catch (err) {
        if (!err?.response) {
            alert('No Server Response Navbar');
          } else if (err.response?.status === 401) {
            alert('Authorization token is missing');
          } else {
            alert("There was an issue in getting username");
          }
    }
}