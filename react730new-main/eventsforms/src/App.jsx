import { useState } from "react";
import { useRef } from "react";
function App ()
{
  const [top, setTop] = useState('60%')
  const [left, setLeft] = useState('60%')
  const [email, setEmail] = useState("")
  const [username, setUserName] = useState("")
  const [password, setPassword] = useState("")
  const [Confirmpassword, setConfirmPassword] = useState("")
  const [error, setError] = useState("")
  const usernameRef = useRef("");
  const emailRef = useRef("");
  const passwordRef = useRef("") 
  const confirmPasswordRef = useRef("") 
  const buttonStyles = {
    position:"absolute",
    top: top,
    left: left,
     transition:"all 1s ease"
  }
  function changeButtonPosition ()
  {
    setTop(`${Math.round(Math.random()*100)}%`)
     setLeft(`${Math.round(Math.random()*100)}%`)
  }
  function handleValidateData ()
  {
    if (username.trim().length < 8)
    {
      setError("username must be atleast 8 characters");
      return false
    }
    if (!(email.match('^[A-Za-z0-9]+@[A-Za-z]+\.[A-Za-z]{2,}$')))
    {
      setError("Email is Not Valid");
      return false
    }
    if (password != Confirmpassword)
    {
      setError("Passwords are not matching");
      return false;
    }
    return true;
  }
  const handleSubmit = (e) =>
  {
    e.preventDefault();
    const isGood = handleValidateData();
    if (isGood)
    {
      fetch(`https://ca35a9a54c58321286e5.free.beeceptor.com/api/users`, {
				method: "POST",
				body: JSON.stringify({
					username: username,
					email: email,
					password: password,
				}),
			})
				.then((res) => {
					if (res.ok) alert("Successfuly submitted the data")
					else alert("Please check the api ,network error")
				})
				.catch((err) => console.log(err))
			setUserName("")
			setEmail("")
			setPassword("")
			Confirmpassword("")
    }
    else
    {
      alert(error)
    }
  }
  const handleSubmit2 = (e) => {
		e.preventDefault()
	  console.log(usernameRef.current.value,emailRef.current.value,passwordRef.current.value)
			fetch(`https://ca35a9a54c58321286e5.free.beeceptor.com/api/users`, {
				method: "POST",
				body: JSON.stringify({
					username: usernameRef.current.value,
					email: emailRef.current.value,
					password: passwordRef.current.value,
				}),
			})
				.then((res) => {
					if (res.ok) alert("Successfuly submitted the data")
					else alert("Please check the api ,network error")
				})
				.catch((err) => console.log(err))
	}
  return (
		<div>
			<header className=' bg-gray-400 text-white text-5xl text-center py-3'>
				<h1>React events and Forms</h1>
			</header>
			{/* <div className=' h-screen flex flex-col justify-center items-center'>
				<h2 className=" text-green-800 text-7xl ">Do you Like My Classes?</h2>
				<div className=" flex gap-3 m-4">
          <button className="bg-black rounded-2xl text-2xl p-3 text-white">YES</button>
					<button style={buttonStyles} onMouseOver={changeButtonPosition} className="bg-black rounded-2xl text-2xl p-3 text-white">NO</button>
				</div>
      </div> */}
			<div className=' my-4'>
				<h2 className='text-center text-4xl font-bold'>
					Controlled Components Forms
				</h2>
				<form
					className='my-4 flex flex-col justify-center items-center gap-2'
					onSubmit={handleSubmit}>
					<input
						type='text'
						value={username}
						onChange={(e) => setUserName(e.target.value)}
						placeholder='Enter UserName'
						className=' h-10 border-2 border-black p-3 text-2xl w-3/12 rounded-2xl'
					/>
					<input
						type='email'
						value={email}
						onChange={(e) => setEmail(e.target.value)}
						placeholder='Enter Email'
						className=' h-10 border-2 border-black rounded-2xl  p-3 text-2xl w-3/12 '
					/>
					<input
						type='password'
						value={password}
						onChange={(e) => setPassword(e.target.value)}
						placeholder='Enter Password'
						className=' h-10 border-2 border-black rounded-2xl  p-3 text-2xl w-3/12 '
					/>
					<input
						type='password'
						value={Confirmpassword}
						onChange={(e) => setConfirmPassword(e.target.value)}
						placeholder='Re Enter Password'
						className=' h-10 border-2 border-black rounded-2xl  p-3 text-2xl w-3/12 '
					/>
					<button className='bg-black rounded-2xl text-2xl p-3 text-white'>
						submit
					</button>
				</form>
				<h2 className='text-center text-4xl font-bold'>
					UNControlled Components Forms
				</h2>
				<form
					className='my-4 flex flex-col justify-center items-center gap-2'
					onSubmit={handleSubmit2}>
					<input
						type='text'
						ref={usernameRef}
						placeholder='Enter UserName'
						className=' h-10 border-2 border-black p-3 text-2xl w-3/12 rounded-2xl'
					/>
					<input
						type='email'
						ref={emailRef}
						placeholder='Enter Email'
						className=' h-10 border-2 border-black rounded-2xl  p-3 text-2xl w-3/12 '
					/>
					<input
						type='password'
						ref={passwordRef}
						placeholder='Enter Password'
						className=' h-10 border-2 border-black rounded-2xl  p-3 text-2xl w-3/12 '
					/>
					<input
						type='password'
						ref={confirmPasswordRef}
						placeholder='Re Enter Password'
						className=' h-10 border-2 border-black rounded-2xl  p-3 text-2xl w-3/12 '
					/>
					<button className='bg-black rounded-2xl text-2xl p-3 text-white'>
						submit
					</button>
				</form>
			</div>
		</div>
	)
}

export default App
