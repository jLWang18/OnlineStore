import './App.css';

function HomeHeaders() {
  return (
    <div>
      <h1> Jay Jay Mart</h1>
      <p>where you can find what you need</p>
   </div>
  );
}

 function fetchProductList() {
  // when the products is successfully fetched, 
  //return array as the resolved value
  return new Promise((resolve, reject) => {
     // request: products data from the server
     fetch("http://localhost:5000/api/products").then(response => {
      // convert response to json
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      return response.json();
    })
    .then(products => {
      // parsed response into array
      let productList = [];

      products.forEach(product => {
        productList.push(product)
      })
      
      // return array as resolved value
      resolve(productList);
    })
    .catch(error => {
      // handle errors while fetching
      reject(error);
    })
    
  }) 
  
    
}
async function getProductList(callback) {
  try {
    // get productList array
    const productList = await fetchProductList();
    
    // pass the array to the callback
    callback(productList);

  } catch(error) {
    // if fetch is not successful, display an error
    console.log("Error fetching data:", error)
  }
 
}
 function ProductTable() {
  // get the productList array
  getProductList((productList) => {
    console.log("ProductList array received", productList);
  })
  //  getProductList((productList) => {
  //  return (
  //   <table>
  //     <tr>
  //       <th>Product ID</th>
  //       <th>Product Category</th>
  //       <th>Product Name</th>
  //       <th>Price</th>
  //       <th>Quantity</th>
  //     </tr>
  //     <tr>
  //       productList.
  //       <td>1</td>
  //       <td>Food</td>
  //       <td>Hamburger</td>
  //       <td>10</td>
  //     </tr>
  //   </table>
  //  )
  // })

 

  // display in the table
   return (
    <table>
      <tr>
        <th>Product ID</th>
        <th>Product Category</th>
        <th>Product Name</th>
        <th>Price</th>
        <th>Quantity</th>
      </tr>
      <tr>
        <td>1</td>
        <td>Food</td>
        <td>Hamburger</td>
        <td>10</td>
      </tr>
    </table>
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
