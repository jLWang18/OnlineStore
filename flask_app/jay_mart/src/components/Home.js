import useAuth from '../hooks/useAuth.js';
import { useEffect, useState } from "react";
import { fetchUserName } from "../logic/fetch_username.js";
import ProductTable from './ProductTable.js';

function HomeHeaders() {
  const {isLoggedIn} = useAuth();
  const [username, setUsername] = useState("");

  useEffect(() => {
      // if the user is logged in, fetch username. Else, return 
      if (isLoggedIn) {
          fetchUserName(setUsername);
      } else {
          return
      }
      
  }, [isLoggedIn])

    return (
      <div>
        {isLoggedIn ? (
          <>
            <h1> Welcome {username} to Jay Jay Mart!</h1>
            <p>you can find what you need here</p>
          </>
  
        ) : (
          <>
            <h1>Jay Jay Mart</h1>
            <p>you can find what you need here</p>
            <p><i>Notes: Please login before ordering products.</i></p>
          </>
        )}
      </div>
    );
}
  
  
   
  
export default function Home() {
    return (
      <>
      <HomeHeaders/>
      <ProductTable />
      </>
    )
  
  }