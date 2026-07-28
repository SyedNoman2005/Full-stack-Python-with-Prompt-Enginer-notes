function Movie (props)
{
    return (
			<div className='movie'>
				<img
					src={props.imgLink}
					alt={props.title}
				/>
            <h2>{props.title}</h2>
            <p>Released Year :{props.year} </p>
			</div>
		) 
}
export default Movie