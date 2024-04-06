import Cookies from "js-cookie"
import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"

function Login() {
	const [username, setUsername] = useState('')
	const [password, setPassword] = useState('')
	const navigate = useNavigate()

	useEffect(() => {
		const token = Cookies.get('session_token')
		if (token) {
			navigate('/')
		}
	}, [])

	const authenticate = async () => {
		try {
			const response = await fetch('http://localhost:8000/ws/login/', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({
					username: username,
					password: password
				})
			})
			if (!response.ok) {
				throw new Error('Authredicate failed')
			}
			const data = await response.json()
			Cookies.set('session_token', data.session_token)
			navigate('/')
		} catch (error) {
			console.error('HTTP Request error: ', error)
		}
	}

	return (
		<div className="flex justify-center items-center w-screen h-screen">
			<ul className="border rounded-xl p-6 text-2xl shadow flex flex-col gap-8 w-1/4">
				<h1 className="text-4xl uppercase text-center font-bold text-gray-800">webshell</h1>
				<li>
					<h3 className="mb-2 text-gray-700">username</h3>
					<input className="border rounded-md p-1 text-xl w-full"
						type="text" autoComplete="off" value={username}
						onChange={(e) => setUsername(e.target.value)} />
				</li>
				<li>
					<h3 className="text-gray-700">password</h3>
					<input className="border rounded-md p-1 text-xl w-full" 
						type="password" value={password}
						onChange={(e) => setPassword(e.target.value)} />
				</li>
				<li className="text-center bg-cyan-400 rounded-md mt-12 p-1">
					<button onClick={authenticate}>authenticate</button>
				</li>
			</ul>
		</div>
	)
}

export default Login
