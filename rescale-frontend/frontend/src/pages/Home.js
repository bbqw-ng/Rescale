import {useState, useEffect} from 'react'
import { useNavigate } from 'react-router-dom'

function HomePage() {
  const navigate = useNavigate()
  const [recipes, setRecipes] = useState([])

  //Loads the recipe cards once
  useEffect(() => {
    async function getRecipes() {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/recipes`, {
      method: 'GET',
      headers: {'Content-Type': 'application/json'}
      })
    const data = await response.json()
    setRecipes(data)
    }
    getRecipes()
  } ,[])

  return recipes.map((recipe) => (
    <div key={recipe.id}>
      <ul>{recipe.id}</ul>
      {recipe.name}
    </div>
  ))
}


export default HomePage

