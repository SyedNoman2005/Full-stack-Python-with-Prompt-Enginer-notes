import Button from "./components/Button"
import Cartoon from "./components/Cartoon";

const App = () =>
{
  const cartoons = [
    { name: "shinchan", year: 2010 },
    { name: "Doremon", year: 2014 },
    { name:"Tom & Jerry", year:1998}
  ]
  return (
		<>
      <Button color="red" text="Signup" size="lg" />
      <div className=" grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3  m-auto max-w-5xl gap-5">
        {cartoons.map((e) => (
          <Cartoon title={e.name} year={e.year} />
        ))}
      </div>
		</>
	)
}
export default App;