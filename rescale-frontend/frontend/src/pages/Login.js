import { useState } from 'react'
import {useNavigate} from 'react-router-dom'

function Login() {
  const navigate = useNavigate() 
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  const handleSubmit = async() => {
    const response = await fetch(`${process.env.REACT_APP_API_URL}/login`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({email, password}),
    credentials: 'include'
    })
    const data = await response.json()
    console.log(data)
    if (response.ok) {
      navigate("/recipes")
    }
  }

  return (
    <div>
      <h1>Login</h1>
      <input type="email" value={email} onChange={(e) => setEmail(e.target.value)}/>
      <input type="password" value={password} onChange={(e) => setPassword(e.target.value)}/>
      <button onClick={handleSubmit}>Login</button>
      <div>
        <h1>Need an Account?</h1>
        <button onClick={navigate("/register")}>Register</button>
      </div>
    </div>
  )
}

export default Login