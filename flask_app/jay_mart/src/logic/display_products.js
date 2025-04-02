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
  export async function getProductList() {
    try {
      // get productList array
      const productList = await fetchProductList();
      // return the products directly
      return productList
    } catch(error) {
      // if fetch is not successful, display an error
      console.log("Error fetching data:", error)
      return [] 
    }
   
  }

export function getSelectedItems() {
   // reference the table
   let grid = document.getElementById("product-table");

   // refrence the checkboxes
   let checkBoxes = grid.getElementsByTagName("input");
 
   let selectedItems = [];
 
   // loop through the checkboxes
   for (let i = 0; i < checkBoxes.length; i++) {
     if (checkBoxes[i].checked) {
       // select table row element
       let row = checkBoxes[i].parentNode.parentNode;
    
       const item = {
        id: row.cells[1].innerHTML,
        category: row.cells[2].innerHTML,
        name: row.cells[3].innerHTML,
        price: row.cells[4].innerHTML,
        quantity:row.cells[5].innerHTML
       }
       // add item to selectedItems array
       selectedItems.push(item)
     }
   }
   // return selectedItems array
   return selectedItems;
}


export function displayCart(selectedItems) {

  // loop through the array
  for (let i = 0; i < selectedItems.length; i++) {
    // print out selected items
    console.log(selectedItems[i])

  }
  // // reference the table
  // let grid = document.getElementById("product-table");

  // // refrence the checkboxes
  // let checkBoxes = grid.getElementsByTagName("input");

  // // display data in the table
  // let placeholder = document.querySelector("#data-output");
  // let out = "";

  // // loop through the checkboxes
  // for (let i = 0; i < checkBoxes.length; i++) {
  //   if (checkBoxes[i].checked) {
  //     // select table row element
  //     let row = checkBoxes[i].parentNode.parentNode;
  //     console.log(row.cells[1].innerHTML)

  //     out += `
  //        <tr> 
  //         <td>${row.cells[1].innerHTML}</td>
  //         <td>${row.cells[2].innerHTML}</td>
  //         <td>${row.cells[3].innerHTML}</td>
  //         <td>$${row.cells[4].innerHTML}</td>
  //         <td>${row.cells[5].innerHTML}</td>
  //        </tr>`;
  //   }
  // }

  // placeholder.innerHTML = out;
}