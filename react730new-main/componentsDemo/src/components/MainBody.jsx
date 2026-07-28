import './Mainbody.css'
import Movie from './Movie'
function MainBody ()
{
    const movies = [
			{
				title: "KGF",
				year: "2020",
				imgLink:
					"https://m.media-amazon.com/images/M/MV5BM2M0YmIxNzItOWI4My00MmQzLWE0NGYtZTM3NjllNjIwZjc5XkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
			},
			{
				title: "Saahoo",
				year: "2019",
				imgLink:
					"https://upload.wikimedia.org/wikipedia/en/6/6b/Saaho_poster.jpg",
			},
			{
				title: "Vikram",
				year: "2016",
				imgLink:
					"https://m.media-amazon.com/images/M/MV5BMmViYjExY2UtMzZjOS00OGQ2LWEzNWYtNGYxY2NkY2RmMDE3XkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
			},
			{
				title: "Shawshak redemption",
				year: "1998",
				imgLink:
					"https://m.media-amazon.com/images/M/MV5BMDAyY2FhYjctNDc5OS00MDNlLThiMGUtY2UxYWVkNGY2ZjljXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
			},
			{
				title: "Titanik",
				year: "1999",
				imgLink: "",
			},
			{
				title: "Pushpa",
				year: "2019",
				imgLink: "pushpa.jpg",
			},
		]
    return (
			<div>
				<h1>Movies</h1>
				<div className='movies'>
                {
                    movies.map((e) =>
                    (
                        <Movie imgLink={e.imgLink} title={e.title} year={e.year} />
                    ))
                    }
				</div>
			</div>
		)
}
export default MainBody
