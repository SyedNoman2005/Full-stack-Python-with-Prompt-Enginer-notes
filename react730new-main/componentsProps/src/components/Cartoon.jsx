const Cartoon = ({title,year}) =>
{
    return (
        <div className=" p-5 border border-black rounded rounded-3xl flex flex-col gap-2 animate-bounce">
            <h2>{title}</h2>
            <p>{year}</p>
        </div>
    )
}
export default Cartoon;