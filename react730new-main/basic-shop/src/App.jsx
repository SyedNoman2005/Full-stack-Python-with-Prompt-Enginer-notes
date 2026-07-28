import { useState } from "react"
import Products from "./components/Products"
import { ShoppingCart } from "lucide-react"

const App = () =>
{
  const [count,setCount] = useState(0)
  return (
		<>
			<header className=' bg-neutral-700 text-3xl text-white py-5 px-5 flex justify-between items-center'>
				<h2 className=' text-5xl'>
					Basic <span className=' text-blue-500'>Shop</span>
				</h2>
				<div className=" flex justify-center items-center">
          <ShoppingCart /><span className=" absolute top-5 right-1 text-blue-500">{count}</span>
				</div>
			</header>
      <Products counterFn={setCount} count={count} />
      <footer className=" bg-neutral-700 text-2xl text-white text-center py-3">
        This site belongs to xyz&copy;2026. it is made with 💓
      </footer>
		</>
	)
}
export default App