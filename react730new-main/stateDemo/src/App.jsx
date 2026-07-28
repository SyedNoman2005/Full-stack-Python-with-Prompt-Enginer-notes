import './App.css'
import { useState } from 'react'
function App ()
{
  const [x, setX] = useState(1)
  const [t,setT] = useState("")
  return (
    <>
      <input type='text' value={t} onChange={(e)=>setT(e.target.value)}/>
      <p>You Entered: {t}</p>
      <p>{x}</p>
			<button onClick={()=>setX(x-1)}>-</button>
			<button onClick={()=>setX(x+1)}>+</button>
		</>
	)
}
export default App