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

export function handleOrder() {
  // reference the table
  let grid = document.getElementById("myTable");

  // refrence the checkboxes
  let checkBoxes = grid.getElementsByTagName("input");
  let message = "Your cart contains:\n\n"

  // loop through the checkboxes
  for (let i = 0; i < checkBoxes.length; i++) {
    if (checkBoxes[i].checked) {
      // select table row element
      let row = checkBoxes[i].parentNode.parentNode;
     
      // get the value of second row, third row, etc.
      message += "Product ID: " + row.cells[1].innerHTML;
      message += "\nProduct Category: " + row.cells[2].innerHTML;
      message += "\nProduct Name: " + row.cells[3].innerHTML;
      message += "\nPrice: " + row.cells[4].innerHTML;
      message += "\nQuantity: " + row.cells[5].innerHTML;
      message += "\n\n";
    }
  }
  // display products in the console window
  console.log(message);

  // After the user clicks "Add To Cart" button, uncheck all the checkboxes
  for (let i = 0; i < checkBoxes.length; i++) {
    // if the checkbox is checked, uncheck it
    if (checkBoxes[i].checked) {
      checkBoxes[i].checked = false;
    }
  }
}