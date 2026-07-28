import React from 'react'
import {Link} from 'react-router-dom'
function ProjectsPage ()
{
  const projectArr = [
		{
			id: 1,
			name: "Ecommerce Website",
			image:
				"https://www.datocms-assets.com/205/1640011361-react-ecommerce-tutorial.png?auto=format&h=500",
			desc: "",
		},
		{
			id: 2,
			name: "Ecommerce Website2",
			image:
				"https://www.datocms-assets.com/205/1640011361-react-ecommerce-tutorial.png?auto=format&h=500",
			desc: "",
		},
		{
			id: 3,
			name: "Ecommerce Website3",
			image:
				"https://www.datocms-assets.com/205/1640011361-react-ecommerce-tutorial.png?auto=format&h=500",
			desc: "",
		},
	]
  return (
		<div className='my-10'>
			<h2 className=' text-5xl text-center text-blue-500'>My Projects</h2>
			<div className='grid grid-cols-3 gap-5'>
				{projectArr.map((e) => (
					<div key={e.id} className=' flex flex-col gap-3 rounded-2xl p-5 justify-center items-center'>
						<img
							src={e.image}
							alt={e.name}
						/>
						<h2>{e.name}</h2>
						<button className='border-2 rounded-2xl p-3 border-blue-500 hover:bg-blue-500 hover:text-white'>
							<Link to={`/project/${e.id}?pname=${e.name}&pimage=${e.image}&pdesc=${e.desc}`}>See Live</Link>
						</button>
					</div>
				))}
			</div>
		</div>
	)
}

export default ProjectsPage
