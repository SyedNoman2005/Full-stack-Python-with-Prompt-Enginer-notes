import React from 'react'
import {Link} from 'react-router-dom'
function Header() {
  return (
		<header className='bg-black text-white py-2 px-5 flex justify-between items-center'>
			<h2 className=' text-5xl text-white'>
				PRA<span className='text-blue-500'>SAD</span>
      </h2>
      <nav>
        <ul className='flex justify-center items-center gap-5'>
          <li><Link to="" className='text-2xl hover:text-blue-500'>Home</Link></li>
          <li><Link to="/about" className='text-2xl hover:text-blue-500'>About</Link></li>
          <li><Link to="/projects" className='text-2xl hover:text-blue-500'>Projects</Link></li>
          <li><Link to="/contact" className='text-2xl hover:text-blue-500'>Contact</Link></li>
        </ul>
      </nav>
		</header>
	)
}

export default Header
