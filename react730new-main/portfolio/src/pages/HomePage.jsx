import React from 'react'
import { Link } from 'react-router-dom'
import Slider from "react-slick"
import "slick-carousel/slick/slick.css"
import "slick-carousel/slick/slick-theme.css"
function HomePage ()
{
  let settings = {
    dots: true,
    arrows: true,
    autoplay:true,
    infinite: true,
    autoplaySpeed:2000,
		speed: 500,
		slidesToShow: 3,
		slidesToScroll: 1,
	}
  return (
		<div>
			<section className=' flex justify-between gap-10 items-center my-5'>
				<div className='flex flex-col gap-3'>
					<h1 className=' text-5xl font-bold'>
						Hi, This is Prasad.
						<br /> I'm a{" "}
						<span className=' text-blue-500'>Frontend Engineer</span>.
					</h1>
					<p className='text-2xl'>
						React Engineer specializing in high-performance UI and animated
						interfaces.
					</p>
					<div className='flex gap-2'>
						<button className='rounded-2xl bg-blue-500 text-white p-4 text-center'>
							Contact Me
						</button>
						<button className='rounded-2xl border border-blue-500 text-black p-4 text-center '>
							<Link to='/projects'>See My Projects</Link>
						</button>
					</div>
				</div>
				<div>
					<img
						src='https://avatars.githubusercontent.com/u/137625133?v=4'
						alt=''
						className=' h-full w-full object-contain'
						style={{ borderRadius: "50%" }}
					/>
				</div>
			</section>
			<section>
				<Slider {...settings}>
					<div>
						<h3>1</h3>
					</div>
					<div>
						<h3>2</h3>
					</div>
					<div>
						<h3>3</h3>
					</div>
					<div>
						<h3>4</h3>
					</div>
				</Slider>
			</section>
		</div>
	)
}

export default HomePage
