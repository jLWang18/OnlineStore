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

  export function displayTable() {
    // get the productList array
    getProductList((productList) => {
      // display data in the table
      let placeholder = document.querySelector("#data-output");
      let out = "";
      productList.forEach(product => {
        out += `
           <tr>
              <td><input type="checkbox"></td>
              <td>${product.product_id}</td>
              <td>${product.product_category}</td>
              <td>${product.product_name}</td>
              <td>$${product.product_price}</td>
              <td>${product.in_stock_quantity}</td>
           </tr>
          `;
      })
      placeholder.innerHTML = out;
   })
}

export function displayCart() {
  // reference the table
  let grid = document.getElementById("product-table");

  // refrence the checkboxes
  let checkBoxes = grid.getElementsByTagName("input");

  // display data in the table
  let placeholder = document.querySelector("#data-output");
  let out = "";

  // loop through the checkboxes
  for (let i = 0; i < checkBoxes.length; i++) {
    if (checkBoxes[i].checked) {
      // select table row element
      let row = checkBoxes[i].parentNode.parentNode;
      console.log(row.cells[1].innerHTML)

      out += `
         <tr> 
          <td>${row.cells[1].innerHTML}</td>
          <td>${row.cells[2].innerHTML}</td>
          <td>${row.cells[3].innerHTML}</td>
          <td>$${row.cells[4].innerHTML}</td>
          <td>${row.cells[5].innerHTML}</td>
         </tr>`;
    }
  }

  placeholder.innerHTML = out;
}