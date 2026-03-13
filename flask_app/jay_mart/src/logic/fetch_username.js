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