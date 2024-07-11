import './App.css';
import {displayTable, handleOrder} from './productTable.js';
import { useEffect } from 'react';

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

function Home() {
  return (
    <>
      <HomeHeaders />
      <ProductTable />
   </>
  );

}
function App() {
  return <Home />
}

export default App;
