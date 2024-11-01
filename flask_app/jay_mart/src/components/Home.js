import ProductTable from './ProductTable.js';

function HomeHeaders() {
    return (
      <div>
        <h1>Jay Jay Mart</h1>
        <p>where you can find what you need</p>
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