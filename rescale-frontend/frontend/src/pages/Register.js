import { useState } from 'react'
import {useNavigate} from 'react-router-dom'


function Register() {
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPass, setConfirmPass] = useState('')

  const handleSubmit = async() => {
    if (password !== confirmPass) {
      console.log("passwords do not match")
      return
    }

    const response = await fetch(`${process.env.REACT_APP_API_URL}/register`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({email,password}),
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
      <h1>Register</h1>
      <input type="email" value={email} onChange={(e) => setEmail(e.target.value)}/>
      <input type="password" value={password} onChange={(e) => setPassword(e.target.value)}/>
      <input type="password" value={confirmPass} onChange={(e) => setConfirmPass(e.target.value)}/>
      <button onClick={handleSubmit}>Register</button>
    </div>
  )
}

export default Register 