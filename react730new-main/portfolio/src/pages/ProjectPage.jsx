import React from 'react'
import { useParams } from 'react-router-dom'
import { useSearchParams } from 'react-router-dom'
function ProjectPage ()
{
    const { id } = useParams()
    const [searchParams] = useSearchParams()
    const pname = searchParams.get('pname');
    const pimage = searchParams.get("pimage");
    const pdesc = searchParams.get("pdesc")
  return (
      <div>
          <img src={pimage} alt={pname} />
          <h1>Project Page: {pname}</h1>
          <p>Description:{pdesc}</p>
    </div>
  )
}

export default ProjectPage
