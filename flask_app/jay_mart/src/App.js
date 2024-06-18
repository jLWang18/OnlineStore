import './App.css';
import { useEffect, useMemo } from 'react';
import { useTable } from "react-table";

function HomeHeaders() {
  return (
    <div>
      <h1> Jay Jay Mart</h1>
      <p>where you can find what you need</p>
   </div>
  );
}

async function getProductList() {

  try {
    // request: products data from the server
    const response = await fetch("http://localhost:5000/api/products");

    // convert response to JSON
    const products = await response.json();

   // console.log(products);

    let productList = [];

    products.forEach(product => {
      productList.push(product)
    })

    //console.log(productList);

    return productList;

  } catch (err) {
    console.log(err);
    return null;
  }
    
}
// async function receiveList() {
//    // get product list
//    const productList = await getProductList();
//    return productList
// }
async function ProductTable() {
  // when I did this, I got
  // Error: Objects are not valid as a React child (found: [object Promise]). If you meant to render a collection of children, use an array instead.
   const productList = await getProductList();
   
   // aku udah coba call method receiveList as a way to return the productList. However, it returns Promise object 
   //const productList = receiveList();

  console.log("Inside ProductTable function")
  console.log(productList);

  const data = useMemo(() => productList, []);

  // define table columns
  const columns = useMemo(() => [
    {
      Header: "Product ID",
      accessor: "product_id",
    },
    {
      Header: "Product Category",
      accessor: "product_category",
    },
    {
      Header: "Product Name",
      accessor: "product_name",
    },
    {
      Header: "Price",
      accessor: "product_price",
    },
    {
      Header: "Quantity",
      accessor: "in_stock_quantity",
    },
  ], []);

  // create product table with these table functions
  const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow} = useTable(columns, data);


  // a table must contains theaders and tbody
   return (
    <div>
      <table {...getTableProps()}>
        <thead>
          {headerGroups.map((headerGroup) => (
            <tr {...headerGroup.getHeaderGroupProps()}>
              {headerGroup.headers.map((column) => (
                <th {...column.getHeaderProps()}>
                  {column.render("Header")}
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody {...getTableBodyProps()}>
          {rows.map((row) => {
            prepareRow(row)
            return (
              <tr {...row.getRowProps()}>
                {row.cells.map((cell) => (
                  <td {...cell.getCellProps()}> {cell.render("Cell")} </td>
                ))}

              </tr>
            ) 
          })}

        </tbody>
      </table>
    </div>

   ); 


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
